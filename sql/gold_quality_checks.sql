-- Representative post-build checks for the Gold layer.
select * from gold.daily_sales where net_revenue < 0;
select order_date, country_code, count(*) from gold.daily_sales group by 1,2 having count(*) > 1;
