{{ config(materialized='table') }}

with predicted as (
    select 
        date,
        close,
        sentiment_score,
        tweet_count,
        lag_1_sentiment,
        avg_3d_sentiment,
        avg_7d_close,
        weighted_impact,

        -- Manually coded linear regression formula
        -6.904662 + (6.224183 * SENTIMENT_SCORE) + 
        (0.002950 * TWEET_COUNT) + (4.921648 * LAG_1_SENTIMENT) + 
        (28.557330 * AVG_3D_SENTIMENT) + (1.016338 * AVG_7D_CLOSE)
        as predicted_price

    from {{ ref('sentiment_features_final') }}
)

select 
    date,
    close,
    predicted_price
from predicted
