select
    brands_tags,
    count(*) as nb_products,
    round(avg(additives_n), 2) as avg_additives,
    max(additives_n) as max_additives,
    sum(additives_n) as total_additives,
    round(avg(case when nutriscore_grade = 'a' then 1
                   when nutriscore_grade = 'b' then 2
                   when nutriscore_grade = 'c' then 3
                   when nutriscore_grade = 'd' then 4
                   when nutriscore_grade = 'e' then 5
                   else null end), 2) as avg_nutriscore_score,
    mode() within group (order by nutriscore_grade) as most_common_nutriscore
from {{ ref('stg_products') }}
group by brands_tags
order by avg_additives desc
