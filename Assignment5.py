# In Cloud Composer, add snowflake-connector-python to PYPI Packages
from airflow import DAG
from airflow.models import Variable
from airflow.decorators import task
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook 

from datetime import datetime
import requests
import pandas as pd


def return_snowflake_conn():
    # Initialize the SnowflakeHook
    hook = SnowflakeHook(snowflake_conn_id='snowflake_conn')
    conn = hook.get_conn()
    return conn.cursor()


@task
def extract():
    ALPHA_VANTAGE_API_KEY = Variable.get('ALPHA_VANTAGE_API_KEY')
    STOCK_SYMBOL = "NVDA"

    # Alpha Vantage API URL
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_SYMBOL}&apikey={ALPHA_VANTAGE_API_KEY}&outputsize=compact"

    response = requests.get(url)
    data = response.json()

    # Extract "Time Series (Daily)" data
    if "Time Series (Daily)" not in data:
        raise ValueError("Invalid API response: 'Time Series (Daily)' key not found.")
    
    return {"symbol": STOCK_SYMBOL, "data": data["Time Series (Daily)"]}


@task
def transform(extracted_data):
    symbol = extracted_data["symbol"]
    time_series = extracted_data["data"]

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(time_series, orient="index")
    df.reset_index(inplace=True)
    df.columns = ["date", "open", "high", "low", "close", "volume"]

    # Convert data types and ensure JSON compatibility 
    df["date"] = pd.to_datetime(df["date"]).dt.strftime('%Y-%m-%d')  # Convert to string
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

    # Keep only last 90 days
    records = df.sort_values("date", ascending=False).head(90)
    
    return {"symbol": symbol, "records": records.to_dict(orient="records")}


@task
def load(transformed_data, target_table):
    cur = return_snowflake_conn()
    symbol = transformed_data["symbol"]
    records = transformed_data["records"]

    try:
        cur.execute("BEGIN;")  # Start transaction

        # Selecting the database
        cur.execute("CREATE DATABASE IF NOT EXISTS mydatabase")

        # Creating schema if it doesn't exist
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw")

        # Creating table inside the 'raw' schema
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {target_table} (
            symbol STRING NOT NULL,
            date DATE NOT NULL,
            open FLOAT,
            high FLOAT,
            low FLOAT,
            close FLOAT,
            volume FLOAT,
            PRIMARY KEY (symbol, date)
        )
        """
        cur.execute(create_table_query)

        print(f"Table '{target_table}' created or already exists.")

        # Deleting only existing records for the given symbol (FIXED)
        delete_query = f"DELETE FROM {target_table} WHERE symbol = '{symbol}'"
        cur.execute(delete_query)

        # Inserting new records
        insert_query = f"""
            INSERT INTO {target_table} (symbol, date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        for record in records:
            cur.execute(insert_query, (
                symbol,
                record["date"],  # Already a string
                record["open"],
                record["high"],
                record["low"],
                record["close"],
                record["volume"]
            ))

        cur.execute("COMMIT;")  # Commit transaction
        print("Data inserted successfully!")

    except Exception as e:
        cur.execute("ROLLBACK;")  # Rollback in case of an error
        print("Error occurred:", e)
        raise e


with DAG(
    dag_id='Stock_Alpha_Vantage',
    start_date=datetime(2025, 2, 21),
    catchup=False,
    tags=['ETL'],
    schedule_interval='0 2 * * *' 
) as dag:
    target_table = "raw.stock_data"

    data = extract()
    transformed_data = transform(data)
    load(transformed_data, target_table)
