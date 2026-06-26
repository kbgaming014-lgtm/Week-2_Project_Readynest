# 📊 ReadyNest Week 2 — Customer Insights & Recommendation Project

**Analyze. Understand. Suggest. Grow.**

> *Enterprise Customer Intelligence Pipeline built on E-Commerce Orders Dataset using Python, DuckDB, SQL & Matplotlib*
> 
> **Abhijay | B.Tech 2nd Semester | Chandigarh Engineering College, Jhanjeri, Mohali**  
> **Reference: RN-2026-DA-W2-ABJ001**

---

## 📌 Project Overview

This repository contains the complete **Week 2 Data Analytics deliverables** for the ReadyNest Internship. The project performs end-to-end customer intelligence analysis — from raw data ingestion to actionable business recommendations — using a custom E-Commerce Orders dataset with **8,500 transactions** across **1,200 customers**, **20 products**, **5 categories**, and **5 regions of India**.

---

## 👨‍💻 Author

| Field | Detail |
|---|---|
| **Name** | Abhijay |
| **Programme** | B.Tech — 2nd Semester |
| **Institute** | Chandigarh Engineering College, Jhanjeri, Mohali |
| **Project** | Customer Insights & Recommendation Dashboard |
| **Reference** | RN-2026-DA-W2-ABJ001 |

---

## 📂 Repository Structure

```
Week-2_Project_Readynest/
├── README.md
├── Abhijay_Week2_Report.pdf
├── Dashboard Visuals & Assets/
│   ├── Executive_Overview.png
│   ├── Customer_Engagement_Analytics.png
│   ├── Product_Performance.png
│   ├── Customer_Segmentation.png
│   ├── Regional_Analysis.png
│   └── Business_Suggestions.png
└── Source Datasets/
    ├── pipeline.py               # Step 1: Data generation & DuckDB ingestion
    ├── transform.py              # Step 2: Cleaning, segmentation & BI aggregations
    ├── advanced_analytics.py     # Step 3: RFM, recommendations, retention, churn
    ├── customers_raw.csv
    ├── orders_raw.csv
    ├── bi_monthly_trends.csv
    ├── bi_category.csv
    ├── bi_top_products.csv
    ├── bi_region.csv
    ├── bi_customer_segments.csv
    ├── bi_shipping.csv
    ├── p2_rfm_scores.csv
    ├── p3_recommendations.csv
    ├── p4_retention.csv
    ├── p5_churn_risk.csv
    ├── p5_churn_summary.csv
    └── p6_business_suggestions.csv
```

---

## ⚙️ Data Pipeline Architecture

```
Raw Data Generation
        │
        ▼
   pipeline.py ──► DuckDB (readynest_w2.db)
        │               │
        ▼               ▼
  transform.py    advanced_analytics.py
        │               │
        ▼               ▼
  bi_*.csv files   p2_* to p6_* CSVs
        │               │
        └───────┬───────┘
                ▼
      Dashboard Visuals (Matplotlib)
                │
                ▼
      PDF Intelligence Report
```

---

## 📊 Key KPIs

| Metric | Value |
|---|---|
| Total Customers | 1,196 |
| Total Sales | ₹3.12 Crore |
| Total Orders | 8,500 |
| Avg Order Value | ₹3,666 |
| Total Profit | ₹78.4 Lakh |
| Profit Margin | 25.2% |

---

## 👥 Customer Segmentation (RFM)

| Segment | Customers | Revenue Share | Avg Orders |
|---|---|---|---|
| **High Value** | 4 | ~0.8% | 15+ orders |
| **Medium Value** | 873 | **84.6%** | 6–14 orders |
| **Low Value** | 319 | 14.6% | 1–5 orders |

---

## 🚨 Churn Risk Analysis

| Risk Tier | Customers | Avg LTV | Action |
|---|---|---|---|
| Loyal | 487 | ₹35,853 | Reward programs |
| Stable | 619 | ₹20,971 | Upsell campaigns |
| At Risk | 79 | ₹8,581 | Re-engagement coupons |
| One-Time | 11 | ₹4,148 | Win-back emails |

---

## 📈 Dashboard Pages (6 Visuals)

### 1. Executive Overview
![Executive Overview](Dashboard%20Visuals%20%26%20Assets/Executive_Overview.png)

### 2. Customer Engagement Analytics
![Customer Engagement](Dashboard%20Visuals%20%26%20Assets/Customer_Engagement_Analytics.png)

### 3. Product Performance
![Product Performance](Dashboard%20Visuals%20%26%20Assets/Product_Performance.png)

### 4. Customer Segmentation Deep Dive
![Segmentation](Dashboard%20Visuals%20%26%20Assets/Customer_Segmentation.png)

### 5. Regional Sales Analysis
![Regional](Dashboard%20Visuals%20%26%20Assets/Regional_Analysis.png)

### 6. Business Suggestions
![Suggestions](Dashboard%20Visuals%20%26%20Assets/Business_Suggestions.png)

---

## 💡 Top 7 Business Suggestions

**#1 Customer Retention** — Launch loyalty rewards targeting 'At Risk' customers. Offer 15% cashback on 4th purchase.  
*Impact: Convert 20% At-Risk to Stable → +₹8.2L revenue*

**#2 Product Bundling** — Bundle Electronics + Books (highest co-purchase). Create 'Student Starter Packs'.  
*Impact: Increase basket size 18% → +₹4.5L revenue*

**#3 Regional Expansion** — West region has highest AOV. Open Mumbai warehouse to reduce delivery from 5→2 days.  
*Impact: Reduce Standard Delivery churn 25% in West*

**#4 Shipping Upgrade** — Offer free Express upgrade on orders above ₹3,000 to improve ratings.  
*Impact: Improve NPS +12 points, repeat orders +8%*

**#5 Furniture EMI** — Introduce EMI options + virtual room visualizer for Furniture (highest AOV: ₹6,200).  
*Impact: +30% Furniture conversion → +₹12L revenue*

**#6 Onboarding Flow** — Send personalized coupon within 7 days of first purchase to Low Value customers.  
*Impact: Improve 1st-to-2nd order conversion from 32% to 50%*

**#7 Women's Collection** — Women show 12% higher avg rating. Launch dedicated curated 'Women's Collection' page.  
*Impact: Women segment revenue share from 38% to 48%*

---

## 🛠️ Installation & Execution

```bash
# Install dependencies
pip install duckdb pandas numpy matplotlib reportlab openpyxl

# Step 1: Generate data & load into DuckDB
python "Source Datasets/pipeline.py"

# Step 2: Clean, segment & export BI CSVs
python "Source Datasets/transform.py"

# Step 3: Advanced analytics (RFM, churn, recommendations)
python "Source Datasets/advanced_analytics.py"
```

---

## 🎓 Learning Outcomes

- SQL-based data engineering with **DuckDB**
- **RFM Customer Segmentation** methodology
- **Churn Risk Modelling** (4-tier classification)
- **Product Co-purchase Recommendation** engine
- **Cohort Retention Analysis**
- Multi-page **Dashboard Visualization** with Matplotlib
- Actionable **Business Intelligence** reporting

---

## 🔮 Future Scope

- Real-time dashboard with Streamlit/Dash
- ML-based churn prediction (Logistic Regression / XGBoost)
- Collaborative filtering recommendation engine
- Geo-spatial heat map with city-level data
- Automated weekly email reporting pipeline

---

⭐ *If this project helped you, consider starring the repo!*

---

*ReadyNest Data Analytics Internship | Week 2 | Abhijay | CEC Jhanjeri, Mohali*
