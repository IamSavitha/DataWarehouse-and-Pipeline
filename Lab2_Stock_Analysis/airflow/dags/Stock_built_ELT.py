from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.decorators import task
from airflow.hooks.base import BaseHook
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from datetime import datetime
import yfinance as yf
import pandas as pd

DBT_PROJECT_DIR = "/opt/airflow/dbt"

conn = BaseHook.get_connection('snowflake_conn')

def return_snowflake_conn():
    hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')
    return hook.get_conn().cursor()

@task
def extract_and_load():
    stocks = ["NVDA", "AAPL"]
    data = {}

    for stock in stocks:
        ticker = yf.Ticker(stock)
        df = ticker.history(period="180d")
        df.reset_index(inplace=True)
        df.rename(columns={"Date": "date", "Open": "open", "High": "high", 
                           "Low": "low", "Close": "close", "Volume": "volume"}, inplace=True)
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df["volume"] = df["volume"].fillna(0).astype(int)
        df["symbol"] = stock
        data[stock] = df

    df_final = pd.concat(data.values(), ignore_index=True)
    records = df_final.to_dict(orient="records")

    cur = return_snowflake_conn()
    cur.execute("BEGIN;")
    cur.execute("CREATE DATABASE IF NOT EXISTS USER_DB_SWAN")
    cur.execute("CREATE SCHEMA IF NOT EXISTS RAW")

    target_table = "raw.stock_data"
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {target_table} (
        symbol STRING NOT NULL,
        date DATE NOT NULL,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume INT,
        PRIMARY KEY (symbol, date)
    )"""

    cur.execute(create_table_query)
    cur.execute(f"DELETE FROM {target_table}")

    insert_query = f"""
        INSERT INTO {target_table} (symbol, date, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    for record in records:
        cur.execute(insert_query, (
            record["symbol"], record["date"], record["open"],
            record["high"], record["low"], record["close"], record["volume"]
        ))

    cur.execute("COMMIT;")

with DAG(
    "stock_data_etl_dbt",
    start_date=datetime(2025, 4, 21),
    description="DAG for extracting stock data, loading into Snowflake, and running dbt transformations (moving averages, RSI)",
    schedule="0 3 * * *",
    catchup=False,
    default_args={
        "env": {
            "DBT_USER": conn.login,
            "DBT_PASSWORD": conn.password,
            "DBT_ACCOUNT": conn.extra_dejson.get("account"),
            "DBT_SCHEMA": conn.schema,
            "DBT_DATABASE": conn.extra_dejson.get("database"),
            "DBT_ROLE": conn.extra_dejson.get("role"),
            "DBT_WAREHOUSE": conn.extra_dejson.get("warehouse"),
            "DBT_TYPE": "snowflake"
        }
    },
) as dag:

    load_task = extract_and_load()

    print_env = BashOperator(
    task_id="debug_env",
    bash_command='echo $DBT_USER $DBT_ACCOUNT $DBT_ROLE $DBT_DATABASE $DBT_WAREHOUSE $DBT_SCHEMA',)

    dbt_run = BashOperator(
    task_id="dbt_run_transformations",
    bash_command=f"/home/airflow/.local/bin/dbt run --select models/intermediate/moving_averages models/intermediate/rsi --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"/home/airflow/.local/bin/dbt test --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    )

    dbt_snapshot = BashOperator(
        task_id="dbt_snapshot",
        bash_command=f"/home/airflow/.local/bin/dbt snapshot --profiles-dir {DBT_PROJECT_DIR} --project-dir {DBT_PROJECT_DIR}",
    )

    load_task >> print_env >> dbt_run >> dbt_test >> dbt_snapshot
