"""
02_load_to_sql.py
Load the cleaned dataset into a SQLite database (retail.db) as a proper
'sales' table so all downstream analysis is done via SQL, not just Pandas.
"""
import pandas as pd
import sqlite3

df = pd.read_csv("../data/online_retail_II_clean.csv", parse_dates=["InvoiceDate"])

conn = sqlite3.connect("../data/retail.db")
df.to_sql("sales", conn, if_exists="replace", index=False)

conn.execute("CREATE INDEX idx_stockcode ON sales(StockCode)")
conn.execute("CREATE INDEX idx_invoicedate ON sales(InvoiceDate)")
conn.commit()

cur = conn.execute("SELECT COUNT(*) FROM sales")
print("Rows loaded into SQLite 'sales' table:", cur.fetchone()[0])
conn.close()
