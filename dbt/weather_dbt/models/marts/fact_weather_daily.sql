{{ config(materialized='table') }}
select c.city_key, cast(to_char(s.weather_date, 'YYYYMMDD') as integer) as date_key,
    s.temp_max, s.temp_min, s.precipitation_sum, s.windspeed_max
from {{ ref('stg_weather') }} s
join {{ ref('dim_city') }} c on s.city_name = c.city_name