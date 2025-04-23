with moving_avg as (
    select * from {{ ref('moving_averages') }}
),

rsi as (
    select * from {{ ref('rsi') }}
)

select
    ma.symbol,
    ma.date,
    ma.volume,
    ma.close,
    ma.ma_5,
    ma.ma_10,
    ma.ma_20,
    rsi.rsi_14
from moving_avg ma
left join rsi on ma.symbol = rsi.symbol and ma.date = rsi.date
