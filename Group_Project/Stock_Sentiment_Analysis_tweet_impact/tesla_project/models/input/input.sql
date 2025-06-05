-- models/input.sql
{{ config(materialized='table') }}

WITH raw_data AS (
    SELECT *
    FROM {{ source('raw', 'final_raw_table') }}
),
features AS (
    SELECT
        date,
        sentiment_score,
        tweet_count,
        total_likes,
        open,
        close,
        volume,
        LAG(sentiment_score, 1) OVER (ORDER BY date) AS lag_1_sentiment,
        AVG(sentiment_score) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS avg_3d_sentiment,
        AVG(close) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS avg_7d_close,
        sentiment_score * tweet_count AS weighted_impact,
        ((close - open) / NULLIF(open, 0)) * 100 AS price_change_pct
    FROM raw_data
)

SELECT *
FROM features
