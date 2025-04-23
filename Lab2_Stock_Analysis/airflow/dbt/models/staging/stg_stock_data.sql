{{ config(materialized='view') }}

SELECT
    *
FROM {{ source('raw', 'stock_data') }}
