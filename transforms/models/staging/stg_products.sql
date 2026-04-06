select
    code,
    product_name,
    brands_tags,
    countries_en,
    additives_n,
    additives_tags,
    nutriscore_grade,
    nova_group,
    completeness
from raw_products
where
    code is not null
    and brands_tags is not null
    and additives_n is not null
    and additives_n > 0
