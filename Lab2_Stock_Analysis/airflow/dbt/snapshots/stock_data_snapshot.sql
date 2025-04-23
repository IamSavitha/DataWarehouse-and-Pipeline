{% snapshot stock_data_snapshot %}

{{
    config(
      target_database='USER_DB_SWAN',
      target_schema='snapshots',
      unique_key='symbol || date',
      strategy='timestamp',
      updated_at='date'
    )
}}

select * from {{ source('raw', 'stock_data') }}

{% endsnapshot %}
