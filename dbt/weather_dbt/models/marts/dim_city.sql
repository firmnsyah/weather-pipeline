{{ config(materialized='table') }}
select
    row_number() over(order by city_name) as city_key, city_name
from (select distinct city_name from {{ ref('stg_weather') }}) c