-- Top products by revenue, restricted to genuine recurring products:
-- excludes admin/fee codes (POSTAGE, DOTCOM POSTAGE, Manual, Bank Charges, etc.)
-- and requires at least 30 distinct orders so a single bulk purchase can't
-- masquerade as sustained demand.
SELECT
    StockCode,
    Description,
    ROUND(SUM(Revenue), 2)  AS total_revenue,
    SUM(Quantity)           AS total_units,
    COUNT(DISTINCT Invoice) AS num_orders
FROM sales
WHERE StockCode NOT IN ('POST','DOT','M','BANK CHARGES','AMAZONFEE','CRUK','C2','PADS','S','D')
GROUP BY StockCode, Description
HAVING COUNT(DISTINCT Invoice) >= 30
ORDER BY total_revenue DESC
LIMIT 15;
