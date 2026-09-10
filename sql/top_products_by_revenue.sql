-- Top 15 products by total revenue across the full dataset (Dec 2009 - Dec 2011)
SELECT
    StockCode,
    Description,
    ROUND(SUM(Revenue), 2)  AS total_revenue,
    SUM(Quantity)           AS total_units,
    COUNT(DISTINCT Invoice) AS num_orders
FROM sales
GROUP BY StockCode, Description
ORDER BY total_revenue DESC
LIMIT 15;
