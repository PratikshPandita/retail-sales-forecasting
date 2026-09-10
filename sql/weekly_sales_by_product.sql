-- Weekly unit sales per product (SQLite date functions: week starts Monday)
SELECT
    StockCode,
    strftime('%Y-%W', InvoiceDate) AS year_week,
    MIN(date(InvoiceDate, 'weekday 0', '-6 days')) AS week_start,
    SUM(Quantity) AS units_sold,
    ROUND(SUM(Revenue), 2) AS revenue
FROM sales
WHERE StockCode = ?
GROUP BY StockCode, year_week
ORDER BY week_start;
