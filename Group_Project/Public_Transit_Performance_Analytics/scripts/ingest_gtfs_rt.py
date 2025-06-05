import requests
import pandas as pd
import snowflake.connector

def ingest_gtfs_rt_data():
    url = 'https://api.example.com/gtfs-rt/tripupdates.json'
    response = requests.get(url)
    data = response.json()

    df = pd.json_normalize(data['entity'])  # adjust path based on actual structure

    # Connect to Snowflake and insert data
    conn = snowflake.connector.connect(
        user='YOUR_USER',
        password='YOUR_PASSWORD',
        account='YOUR_ACCOUNT'
    )
    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO raw_trip_updates (trip_id, route_id, start_time, delay)
            VALUES (%s, %s, %s, %s)
        """, (
            row['trip.trip_id'],
            row['trip.route_id'],
            row['trip.start_time'],
            row['delay']
        ))
    cur.close()
    conn.close()
