"""
Rebuild the RFM table and cluster profiles from the raw UCI Online Retail file,
using the same cleaning rules as sql_scripts.sql - so you can get the numbers the
original notebook never printed (cluster sizes, average spend, share of revenue).

Raw data: "Online Retail" dataset, UCI Machine Learning Repository
  https://archive.ics.uci.edu/dataset/352/online+retail   (file: Online Retail.xlsx)

Run:  python3 rebuild_rfm.py "Online Retail.xlsx"
Writes: rfm_for_python.csv, cluster_profile.csv
"""
import sys

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

path = sys.argv[1] if len(sys.argv) > 1 else "Online Retail.xlsx"
df = pd.read_excel(path, dtype={"InvoiceNo": str, "StockCode": str})
print(f"Raw rows: {len(df):,}")

# 1. Missing customer IDs can't be segmented
n = len(df); df = df[df["CustomerID"].notna()]
print(f"Removed {n - len(df):,} rows with no CustomerID")

# 2. Duplicates - same partition as the SQL ROW_NUMBER() step (the SQL table stored the date only)
df["InvoiceDay"] = pd.to_datetime(df["InvoiceDate"]).dt.normalize()
n = len(df)
df = df.drop_duplicates(subset=["InvoiceNo", "StockCode", "Quantity", "InvoiceDay", "UnitPrice", "CustomerID"])
print(f"Removed {n - len(df):,} duplicate rows")

# 3. Cancellations, returns, zero-price lines
n = len(df)
df = df[~df["InvoiceNo"].str.startswith("C") & (df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
print(f"Removed {n - len(df):,} cancellation / return / zero-price rows")

df["line_item_total"] = df["Quantity"] * df["UnitPrice"]
print(f"Clean rows: {len(df):,}   Customers: {df['CustomerID'].nunique():,}")

# 4. RFM, with the day after the last sale as 'today' (same as the SQL)
today = df["InvoiceDay"].max() + pd.Timedelta(days=1)
rfm = df.groupby("CustomerID").agg(
    recency=("InvoiceDay", lambda s: (today - s.max()).days),
    frequency=("InvoiceNo", "nunique"),
    monetary=("line_item_total", "sum"),
).reset_index().rename(columns={"CustomerID": "customer_id"})
rfm["customer_id"] = rfm["customer_id"].astype(int)
rfm.to_csv("rfm_for_python.csv", index=False)

# 5. Same clustering as the notebook: log, standardize, K-Means k=4
X = StandardScaler().fit_transform(np.log(rfm[["recency", "frequency", "monetary"]] + 1))
rfm["Cluster"] = KMeans(n_clusters=4, random_state=42, n_init=10).fit_predict(X)

# 6. The profile the original notebook never printed
p = rfm.groupby("Cluster").agg(
    customers=("customer_id", "count"),
    avg_recency_days=("recency", "mean"),
    avg_orders=("frequency", "mean"),
    avg_spend_gbp=("monetary", "mean"),
    total_spend_gbp=("monetary", "sum"),
)
p["pct_customers"] = 100 * p["customers"] / p["customers"].sum()
p["pct_revenue"] = 100 * p["total_spend_gbp"] / p["total_spend_gbp"].sum()
p = p.round(1).sort_values("avg_spend_gbp", ascending=False)
p.to_csv("cluster_profile.csv")
print("\nCluster profile (cluster numbers are arbitrary - name them from the averages):")
print(p.to_string())
print(f"\nOverall average spend per customer: £{rfm['monetary'].mean():,.0f}")
