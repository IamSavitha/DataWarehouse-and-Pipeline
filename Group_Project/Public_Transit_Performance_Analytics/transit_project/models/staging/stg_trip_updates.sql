SELECT
    trip_id,
    route_id,
    start_time,
    delay,
    CURRENT_TIMESTAMP AS ingestion_time
FROM {{ source('transit', 'raw_trip_updates') }}
