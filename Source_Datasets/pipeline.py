"""
pipeline.py — Step 1: Raw Data Generation & DuckDB Ingestion
ReadyNest Week 2 | Customer Insights & Recommendation Project
Abhijay | CEC Jhanjeri, Mohali
"""
import duckdb, random, csv
from datetime import datetime, timedelta

random.seed(99)

N_CUSTOMERS = 1200
N_ORDERS    = 8500
PRODUCTS = [
    ("P001","Wireless Earbuds","Electronics",1299,450),
    ("P002","Laptop Stand","Electronics",899,280),
    ("P003","USB-C Hub","Electronics",699,320),
    ("P004","Mechanical Keyboard","Electronics",2499,190),
    ("P005","Webcam HD","Electronics",1599,210),
    ("P006","Men's Running Shoes","Clothing",1899,380),
    ("P007","Women's Kurta Set","Clothing",999,520),
    ("P008","Denim Jacket","Clothing",1799,290),
    ("P009","Yoga Pants","Clothing",899,410),
    ("P010","Cotton Hoodie","Clothing",1299,360),
    ("P011","Office Desk Chair","Furniture",8999,85),
    ("P012","Bookshelf 5-Tier","Furniture",4599,72),
    ("P013","Study Table","Furniture",6999,63),
    ("P014","Bedside Table","Furniture",3299,91),
    ("P015","Python Programming","Books",499,630),
    ("P016","Data Science Handbook","Books",699,510),
    ("P017","Business Strategy","Books",399,420),
    ("P018","Cricket Bat","Sports",1499,140),
    ("P019","Yoga Mat","Sports",699,310),
    ("P020","Fitness Dumbbells","Sports",1999,175),
]
REGIONS = ["North","South","East","West","Central"]
CITIES  = {
    "North":["Delhi","Chandigarh","Jaipur","Lucknow","Amritsar"],
    "South":["Chennai","Bangalore","Hyderabad","Kochi","Coimbatore"],
    "East":["Kolkata","Bhubaneswar","Patna","Guwahati","Ranchi"],
    "West":["Mumbai","Pune","Ahmedabad","Surat","Nagpur"],
    "Central":["Bhopal","Indore","Raipur","Jabalpur","Gwalior"],
}
SHIP      = ["Standard","Express","Same Day","Overnight"]
AGE_GROUPS= ["18-25","26-35","36-45","46-55","55+"]
GENDERS   = ["Male","Female","Other"]

print("Generating customers...")
customers = []
base_date = datetime(2023, 1, 1)
for i in range(1, N_CUSTOMERS+1):
    reg    = random.randint(1,180)
    region = random.choices(REGIONS, weights=[0.25,0.22,0.18,0.27,0.08])[0]
    city   = random.choice(CITIES[region])
    customers.append({
        "customer_id":       f"CUST{i:04d}",
        "name":              f"Customer_{i:04d}",
        "age_group":         random.choice(AGE_GROUPS),
        "gender":            random.choices(GENDERS, weights=[0.52,0.44,0.04])[0],
        "region":            region,
        "city":              city,
        "registration_date": (base_date + timedelta(days=reg)).strftime("%Y-%m-%d"),
        "is_returning":      random.choice([0,0,0,1,1]),
    })

print("Generating orders...")
orders = []
for i in range(1, N_ORDERS+1):
    cust  = random.choice(customers)
    prod  = random.choices(PRODUCTS, weights=[p[4] for p in PRODUCTS])[0]
    odate = base_date + timedelta(days=random.randint(5,540))
    qty   = random.randint(1,5)
    disc  = round(random.choices([0,0.05,0.10,0.15,0.20,0.25],[0.30,0.20,0.20,0.15,0.10,0.05])[0],2)
    sales = round(prod[3]*(1-disc)*qty, 2)
    profit= round(sales*random.uniform(0.12,0.38), 2)
    ship  = random.choices(SHIP, weights=[0.48,0.28,0.08,0.16])[0]
    ddays = {"Standard":5,"Express":2,"Same Day":0,"Overnight":1}[ship]
    orders.append({
        "order_id":      f"ORD{i:05d}",
        "customer_id":   cust["customer_id"],
        "region":        cust["region"],
        "city":          cust["city"],
        "product_id":    prod[0],
        "product_name":  prod[1],
        "category":      prod[2],
        "quantity":      qty,
        "unit_price":    prod[3],
        "discount":      disc,
        "sales":         sales,
        "profit":        profit,
        "ship_mode":     ship,
        "order_date":    odate.strftime("%Y-%m-%d"),
        "delivery_date": (odate+timedelta(days=ddays)).strftime("%Y-%m-%d"),
        "rating":        random.choices([1,2,3,4,5],weights=[0.05,0.08,0.17,0.38,0.32])[0],
    })

BASE = "/home/claude/week2/Source_Datasets"
with open(f"{BASE}/customers_raw.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=customers[0].keys()); w.writeheader(); w.writerows(customers)
with open(f"{BASE}/orders_raw.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=orders[0].keys()); w.writeheader(); w.writerows(orders)

print("Loading into DuckDB...")
con = duckdb.connect(f"{BASE}/readynest_w2.db")
con.execute("DROP TABLE IF EXISTS fact_orders")
con.execute("DROP TABLE IF EXISTS dim_customers")
con.execute(f"CREATE TABLE dim_customers AS SELECT * FROM read_csv_auto('{BASE}/customers_raw.csv')")
con.execute(f"CREATE TABLE fact_orders    AS SELECT * FROM read_csv_auto('{BASE}/orders_raw.csv')")
r1 = con.execute("SELECT COUNT(*) FROM fact_orders").fetchone()[0]
r2 = con.execute("SELECT COUNT(*) FROM dim_customers").fetchone()[0]
con.close()
print(f"Pipeline complete: {r2} customers, {r1} orders loaded into DuckDB")
