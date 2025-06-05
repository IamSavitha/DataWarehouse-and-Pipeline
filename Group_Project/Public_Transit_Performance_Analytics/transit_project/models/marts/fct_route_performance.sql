SELECT
    route_id,
    DATE(ingestion_time) AS date,
    COUNT(*) AS total_trips,
    AVG(delay) AS avg_delay,
    SUM(CASE WHEN delay <= 300 THEN 1 ELSE 0 END) / COUNT(*) AS on_time_rate
FROM {{ ref('stg_trip_updates') }}
GROUP BY route_id, DATE(ingestion_time)
