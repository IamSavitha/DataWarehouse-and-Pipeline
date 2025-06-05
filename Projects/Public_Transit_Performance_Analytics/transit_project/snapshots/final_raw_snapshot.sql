-- snapshots/final_raw_snapshot.sql
{% snapshot final_raw_snapshot %}
{{
    config(
        target_schema='snapshots',
        unique_key='date',
        strategy='check',
        check_cols=['sentiment_score', 'tweet_count', 'close', 'price_change_pct']
    )
}}

SELECT *
FROM {{ source('raw', 'final_raw_table') }}

{% endsnapshot %}
