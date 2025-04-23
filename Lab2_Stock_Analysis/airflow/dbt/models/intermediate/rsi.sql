with price_changes as (
    select
        symbol,
        date,
        close,
        close - lag(close) over (partition by symbol order by date) as price_diff
    from {{ ref('stg_stock_data') }}
),

gains_losses as (
    select
        symbol,
        date,
        case when price_diff > 0 then price_diff else 0 end as gain,
        case when price_diff < 0 then abs(price_diff) else 0 end as loss
    from price_changes
),

avg_gains_losses as (
    select
        symbol,
        date,
        avg(gain) over (partition by symbol order by date rows between 13 preceding and current row) as avg_gain_14,
        avg(loss) over (partition by symbol order by date rows between 13 preceding and current row) as avg_loss_14
    from gains_losses
),

rsi_calc as (
    select
        symbol,
        date,
        avg_gain_14,
        avg_loss_14,
        case
            when avg_loss_14 = 0 then 100
            else 100 - (100 / (1 + (avg_gain_14 / avg_loss_14)))
        end as rsi_14
    from avg_gains_losses
)

select
    symbol,
    date,
    rsi_14
from rsi_calc
