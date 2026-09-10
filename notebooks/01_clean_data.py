"""
01_clean_data.py
Clean the raw Online Retail II dataset:
- Drop cancelled invoices (Invoice starts with 'C')
- Drop rows with non-positive Quantity or Price
- Drop rows with missing StockCode/Description
- Add a Revenue column (Quantity * Price)
"""
import pandas as pd

df = pd.read_csv("../data/online_retail_II_raw.csv", parse_dates=["InvoiceDate"])
print("Raw shape:", df.shape)

before = len(df)

# Drop cancellations (Invoice starting with 'C')
df = df[~df["Invoice"].astype(str).str.startswith("C")]

# Drop non-positive quantity/price (returns, adjustments, free items)
df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]

# Drop missing product descriptions/codes
df = df.dropna(subset=["StockCode", "Description"])

df["Revenue"] = df["Quantity"] * df["Price"]

print(f"Dropped {before - len(df):,} rows in cleaning ({(before-len(df))/before:.1%})")
print("Clean shape:", df.shape)

df.to_csv("../data/online_retail_II_clean.csv", index=False)
print("Saved cleaned dataset.")
