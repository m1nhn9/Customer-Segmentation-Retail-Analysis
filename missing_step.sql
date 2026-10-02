-- The step missing from sql_scripts.sql.
-- The RFM queries read from `cleaned_retail_data` and a `line_item_total` column, but the
-- script never creates either. Run this after the cleaning DELETEs and before the RFM section.

DROP TABLE IF EXISTS cleaned_retail_data;

CREATE TABLE cleaned_retail_data AS
SELECT
    transaction_id,
    invoice_no,
    stock_code,
    description,
    quantity,
    invoice_date,
    unit_price,
    customer_id,
    country,
    quantity * unit_price AS line_item_total   -- revenue for this line
FROM retail_sales
WHERE customer_id IS NOT NULL      -- already deleted above; kept as a safety net
  AND invoice_no NOT LIKE 'C%'     -- cancellations
  AND quantity > 0                 -- returns / stock adjustments
  AND unit_price > 0;              -- free items and zero-price adjustments

-- Sanity check: rows and customers going into RFM
SELECT COUNT(*) AS rows_in, COUNT(DISTINCT customer_id) AS customers
FROM cleaned_retail_data;

-- Note: the "Guest" query in sql_scripts.sql (sales without a CustomerID) runs AFTER the
-- DELETE that removes null customer IDs, so it always returns 0. Move it above the DELETE.
