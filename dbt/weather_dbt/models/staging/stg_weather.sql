with source as (
    select * from {{ source('raw', 'raw_weather') }}
)

select
    city                as city_name,
    weather_date::date  as weather_date,
    temperature_2m_max  as temp_max,
    temperature_2m_min  as temp_min,
    precipitation_sum   as precipitation_sum,
    windspeed_10m_max   as windspeed_max
from source