WITH base AS (
    SELECT *
    FROM {{ ref('feature_engineering__combined_features') }}
)

SELECT *,
    ROUND(
        0.4 * avg_7d_close + 
        2.5 * sentiment_score + 
        1.8 * weighted_sentiment + 
        0.002 * total_likes + 
        0.003 * tweet_count +
        0.001 * volume / 1000
    , 2) AS predicted_close_price
FROM base
