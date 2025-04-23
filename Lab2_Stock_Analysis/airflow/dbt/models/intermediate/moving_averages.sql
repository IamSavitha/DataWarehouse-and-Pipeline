with base as (
    select
        symbol,
        date,
        volume,
        close,
        avg(close) over (partition by symbol order by date rows between 4 preceding and current row) as ma_5,
        avg(close) over (partition by symbol order by date rows between 9 preceding and current row) as ma_10,
        avg(close) over (partition by symbol order by date rows between 19 preceding and current row) as ma_20
    from {{ ref('stg_stock_data') }}
)

select
    symbol,
    date,
    volume,
    close,
    ma_5,
    ma_10,
    ma_20
from base
