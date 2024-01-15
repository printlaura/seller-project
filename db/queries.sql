-- GET ITEMS BY BRAND MANAGER
select i.id, i.product_title, i.launched_at, b.name
from Item i
left join Brand b
    on i.brand_id = b.id
where i.brand_manager_id = 'Example manager id' -- passed as parameter
;


-- GET SALES ID AND THEIR ORDER DATE BY YEAR AND MONTH
select id, order_date
from SalesOrder
where YEAR(order_date) = CAST('example year' as INT) and MONTH(order_date) = CAST('example month' as INT)
order by order_date DESC
;



-- GET TOTAL SALES PER DATE
select order_date, count(id) as count_of_sales
from SalesOrder
group by order_date
order by order_date DESC
;


-- GET TOTAL ITEMS SOLD PER BRAND BY YEAR AND MONTH
select b.name, b.code, count(io.id) as sales_count, sum(i.sales_margin) as sales_margin
from Brand b
left join Item i
    on b.id = i.brand_id
left join ItemOrdered io
    on i.id = io.item_id
left join SalesOrder so
    on io.order_id = so.id
where YEAR(so.order_date) = CAST('example year' as INT and MONTH(so.order_date) = CAST('example month' as INT)
group by b.name, b.code
;



--ADD NEW BRAND
insert into Brand (name, code, brand_manager_id, acquired_at)
values (upper('brand_name'), 'code', 'brand_manager_id', CURRENT_DATE)
on CONFLICT (name) DO NOTHING;
;



--UPDATE BRAND MANAGER
with
manager as
(
    select id from BrandManager where full_name = 'brand_manager_full_name'
),

brand_cte as
(
    select id from Brand where name = 'brand_name'
)

update Brand
set brand_manager_id = (select id from manager)
from brand b
WHERE Brand.id = brand_cte.id and exists (select 1 from manager)
;



-- DELETE UNSOLD ITEMS
with
sold_items as
(
    select distinct io.item_id
    from ItemOrdered io
    left join SalesOrder so
        on io.order_id = so.id
    where so.order_date >= CURRENT_DATE - INTERVAL '9 months'
)

delete from Item
where id not in (select item_id from sold_items)
;