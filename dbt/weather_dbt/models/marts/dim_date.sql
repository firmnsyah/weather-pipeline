{{ config(materialized='table') }}
select distinct
    cast(to_char(weather_date, 'YYYYMMDD') as integer) as date_key,
    weather_date as full_date,
    extract(year    from weather_date)::int as year,
    extract(month   from weather_date)::int as month,
    extract(day     from weather_date)::int as day,
    extract(dow     from weather_date)::int as day_of_week
from {{ ref('stg_weather') }}