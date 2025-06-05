-- models/sentiment_features_final.sql
{{ config(materialized='table') }}

SELECT 
    date,
    close,
    sentiment_score,
    tweet_count,
    lag_1_sentiment,
    avg_3d_sentiment,
    avg_7d_close,
    weighted_impact,
    volume
FROM {{ ref('input') }}
WHERE close IS NOT NULL
