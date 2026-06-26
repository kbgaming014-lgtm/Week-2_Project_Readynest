"""
transform.py — Step 2: Data Cleaning, Customer Segmentation & BI Aggregations
ReadyNest Week 2 | Customer Insights & Recommendation Project
Abhijay | CEC Jhanjeri, Mohali
"""
import duckdb, pandas as pd, json

BASE = "/home/claude/week2/Source_Datasets"
con  = duckdb.connect(f"{BASE}/readynest_w2.db")

print("=== STEP 2: TRANSFORM & SEGMENT ===")

# ── 1. Cleaned orders ──────────────────────────────────────────────────────────
con.execute("""
CREATE OR REPLACE TABLE cleaned_orders AS
SELECT * FROM fact_orders
WHERE sales > 0 AND profit IS NOT NULL AND customer_id IS NOT NULL
""")
n = con.execute("SELECT COUNT(*) FROM cleaned_orders").fetchone()[0]
print(f"Cleaned orders: {n}")

# ── 2. Customer RFM Segmentation ───────────────────────────────────────────────
con.execute("""
CREATE OR REPLACE TABLE customer_rfm AS
SELECT
    o.customer_id,
    c.region,
    c.city,
    c.age_group,
    c.gender,
    c.is_returning,
    COUNT(DISTINCT o.order_id)          AS frequency,
    SUM(o.sales)                        AS monetary,
    MAX(o.order_date)                   AS last_order_date,
    AVG(o.rating)                       AS avg_rating,
    SUM(o.profit)                       AS total_profit,
    CASE
        WHEN COUNT(DISTINCT o.order_id) >= 15 THEN 'High Value'
        WHEN COUNT(DISTINCT o.order_id) >= 6  THEN 'Medium Value'
        ELSE 'Low Value'
    END AS segment
FROM cleaned_orders o
JOIN dim_customers c ON o.customer_id = c.customer_id
GROUP BY o.customer_id,c.region,c.city,c.age_group,c.gender,c.is_returning
""")
seg = con.execute("""
SELECT segment, COUNT(*) as customers, ROUND(SUM(monetary),2) as total_sales
FROM customer_rfm GROUP BY segment ORDER BY total_sales DESC
""").df()
print("\nCustomer Segments:")
print(seg.to_string(index=False))

# ── 3. Monthly Sales Trend ─────────────────────────────────────────────────────
con.execute("""
CREATE OR REPLACE TABLE bi_monthly AS
SELECT
    STRFTIME(order_date,'%Y-%m') AS month,
    COUNT(DISTINCT order_id)     AS orders,
    ROUND(SUM(sales),2)          AS total_sales,
    ROUND(AVG(sales),2)          AS avg_sales,
    ROUND(SUM(profit),2)         AS total_profit
FROM cleaned_orders
GROUP BY month ORDER BY month
""")
con.execute(f"COPY bi_monthly TO '{BASE}/bi_monthly_trends.csv' (HEADER, DELIMITER ',')")

# ── 4. Category Performance ────────────────────────────────────────────────────
con.execute("""
CREATE OR REPLACE TABLE bi_category AS
SELECT
    category,
    COUNT(DISTINCT order_id)  AS orders,
    ROUND(SUM(sales),2)       AS total_sales,
    ROUND(AVG(sales),2)       AS avg_sale,
    ROUND(SUM(profit),2)      AS total_profit,
    ROUND(AVG(rating),2)      AS avg_rating
FROM cleaned_orders
GROUP BY category ORDER BY total_sales DESC
""")
con.execute(f"COPY bi_category TO '{BASE}/bi_category.csv' (HEADER, DELIMITER ',')")

# ── 5. Top Products ────────────────────────────────────────────────────────────
con.execute("""
CREATE OR REPLACE TABLE bi_top_products AS
SELECT
    product_id, product_name, category,
    COUNT(DISTINCT order_id)  AS orders,
    ROUND(SUM(sales),2)       AS total_sales,
    ROUND(AVG(rating),2)      AS avg_rating
FROM cleaned_orders
GROUP BY product_id,product_name,category
ORDER BY total_sales DESC LIMIT 10
""")
con.execute(f"COPY bi_top_products TO '{BASE}/bi_top_products.csv' (HEADER, DELIMITER ',')")

# ── 6. Region Performance ──────────────────────────────────────────────────────
con.execute("""
CREATE OR REPLACE TABLE bi_region AS
SELECT
    region,
    COUNT(DISTINCT order_id)  AS orders,
    ROUND(SUM(sales),2)       AS total_sales,
    ROUND(AVG(sales),2)       AS avg_order,
    ROUND(SUM(profit),2)      AS total_profit
FROM cleaned_orders
GROUP BY region ORDER BY total_sales DESC
""")
con.execute(f"COPY bi_region TO '{BASE}/bi_region.csv' (HEADER, DELIMITER ',')")

# ── 7. Customer Segments export ────────────────────────────────────────────────
con.execute(f"COPY customer_rfm TO '{BASE}/bi_customer_segments.csv' (HEADER, DELIMITER ',')")

# ── 8. Shipping Analysis ───────────────────────────────────────────────────────
con.execute("""
CREATE OR REPLACE TABLE bi_shipping AS
SELECT
    ship_mode,
    COUNT(*)             AS orders,
    ROUND(SUM(sales),2)  AS total_sales,
    ROUND(AVG(rating),2) AS avg_rating
FROM cleaned_orders GROUP BY ship_mode ORDER BY total_sales DESC
""")
con.execute(f"COPY bi_shipping TO '{BASE}/bi_shipping.csv' (HEADER, DELIMITER ',')")

# ── Save overall stats ────────────────────────────────────────────────────────
stats = con.execute("""
SELECT
    COUNT(DISTINCT order_id)    AS total_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    ROUND(SUM(sales),2)         AS total_sales,
    ROUND(AVG(sales),2)         AS avg_order_value,
    ROUND(SUM(profit),2)        AS total_profit
FROM cleaned_orders
""").df().iloc[0].to_dict()
with open(f"{BASE}/w2_stats.json","w") as f:
    json.dump(stats, f, indent=2)

con.close()
print(f"\nTransform complete! Stats: {stats}")
print("All BI CSVs exported.")
