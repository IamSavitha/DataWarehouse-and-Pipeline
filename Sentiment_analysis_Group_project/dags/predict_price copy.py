from airflow import DAG
from airflow.decorators import task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime


def return_snowflake_conn():
    hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')
    conn = hook.get_conn()
    return conn.cursor()


@task
def train(cur, feature_table, train_view, model_name):
    """
    - Create a view with engineered features
    - Train a regression model on the view
    """
    create_view_sql = f"""
        CREATE OR REPLACE VIEW {train_view} AS
        SELECT
            close AS target,
            sentiment_score,
            weighted_sentiment,
            tweet_count,
            total_likes,
            lag_1_sentiment,
            avg_3d_sentiment,
            avg_7d_close,
            weighted_sentiment * tweet_count AS weighted_tweet_impact,
            volume,
            open,
            high,
            low
        FROM {feature_table}
        WHERE close IS NOT NULL;
    """

    create_model_sql = f"""
        CREATE OR REPLACE SNOWFLAKE.ML.REGRESSION {model_name} (
            INPUT_DATA => SYSTEM$REFERENCE('VIEW', '{train_view}'),
            TARGET_COLNAME => 'target',
            CONFIG_OBJECT => {{
                'model_type': 'XGBoostRegressor',
                'max_iterations': 200
            }}
        );
    """

    try:
        cur.execute(create_view_sql)
        cur.execute(create_model_sql)
        cur.execute(f"CALL {model_name}!SHOW_EVALUATION_METRICS();")
    except Exception as e:
        print("Training failed:", e)
        raise


@task
def predict(cur, model_name, feature_table, prediction_table):
    """
    - Run prediction using trained model and save results
    """
    predict_sql = f"""
        CREATE OR REPLACE TABLE {prediction_table} AS
        SELECT
            date,
            close AS actual_close_price,
            PREDICT(
                MODEL => {model_name},
                DATA => (
                    SELECT
                        sentiment_score,
                        weighted_sentiment,
                        tweet_count,
                        total_likes,
                        lag_1_sentiment,
                        avg_3d_sentiment,
                        avg_7d_close,
                        weighted_sentiment * tweet_count AS weighted_tweet_impact,
                        volume,
                        open,
                        high,
                        low
                    FROM {feature_table}
                )
            ) AS predicted_close_price
        FROM {feature_table};
    """

    try:
        cur.execute(predict_sql)
    except Exception as e:
        print("Prediction failed:", e)
        raise


with DAG(
    dag_id='tsla_stock_price_predictor',
    start_date=datetime(2025, 2, 21),
    catchup=False,
    schedule='30 2 * * *',
    tags=['ML', 'snowflake', 'tsla']
) as dag:

    cur = return_snowflake_conn()

    feature_table = "dev.analytics.feature_enriched_tsla"  # Your final features table
    train_view = "dev.adhoc.tsla_train_view"
    model_name = "dev.analytics.tsla_price_regressor"
    prediction_table = "dev.analytics.tsla_predictions"

    train(cur, feature_table, train_view, model_name)
    predict(cur, model_name, feature_table, prediction_table)
