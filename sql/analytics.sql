USE sales_pipeline;

-- Daily revenue
SELECT DATE(o.order_date) AS sales_date,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.status = 'completed'
GROUP BY DATE(o.order_date)
ORDER BY sales_date;

-- Top products
SELECT p.product_name, p.category,
       SUM(oi.quantity) AS units_sold,
       ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount)), 2) AS revenue
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'completed'
GROUP BY p.product_id, p.product_name, p.category
ORDER BY revenue DESC
LIMIT 10;

-- Customer ranking using a window function
WITH customer_sales AS (
    SELECT c.customer_id, c.customer_name,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) AS revenue
    FROM customers c
    JOIN orders o ON o.customer_id = c.customer_id
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY c.customer_id, c.customer_name
)
SELECT customer_id, customer_name,
       ROUND(revenue, 2) AS revenue,
       RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM customer_sales
ORDER BY revenue_rank
LIMIT 20;

-- Monthly revenue growth
WITH monthly AS (
    SELECT DATE_FORMAT(o.order_date, '%Y-%m-01') AS month,
           SUM(oi.quantity * oi.unit_price * (1 - oi.discount)) AS revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.status = 'completed'
    GROUP BY DATE_FORMAT(o.order_date, '%Y-%m-01')
),
with_previous AS (
    SELECT month, revenue,
           LAG(revenue) OVER (ORDER BY month) AS previous_revenue
    FROM monthly
)
SELECT month,
       ROUND(revenue, 2) AS revenue,
       ROUND(
           100 * (revenue - previous_revenue) / NULLIF(previous_revenue, 0),
           2
       ) AS growth_pct
FROM with_previous
ORDER BY month;
