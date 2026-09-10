"""
03_forecast_top_products.py
For each of the top 5 recurring products (by revenue), build a weekly
demand series via SQL, hold out the last 8 weeks, and fit an exponential
smoothing model, evaluating forecast accuracy (MAE, MAPE) against the
held-out weeks.

Note on seasonality: the dataset spans ~2 years (Dec 2009-Dec 2011).
After removing an 8-week holdout, the training window is under 104 weeks
(two full annual cycles), which statsmodels' own initialization check
flags as insufficient to reliably estimate a 52-week seasonal component.
Rather than force a yearly-seasonal model on data that can't support one,
this uses Holt's trend-only exponential smoothing (level + trend, no
seasonal term). Any Christmas-driven seasonality is instead surfaced
separately in the EDA step as a descriptive finding, not baked into the
forecast itself.
"""
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

conn = sqlite3.connect("../data/retail.db")
weekly_q = open("../sql/weekly_sales_by_product.sql").read()

top15 = pd.read_csv("../reports/top_15_products_clean.csv")
top5 = top15.head(5)

HOLDOUT_WEEKS = 8
results = []

fig, axes = plt.subplots(5, 1, figsize=(10, 14), sharex=False)

for i, row in top5.iterrows():
    code, desc = row["StockCode"], row["Description"]
    s = pd.read_sql(weekly_q, conn, params=(code,))
    s["week_start"] = pd.to_datetime(s["week_start"])
    s = s.sort_values("week_start").reset_index(drop=True)

    # Use a continuous weekly index (fill any gap weeks with 0 units)
    full_idx = pd.date_range(s["week_start"].min(), s["week_start"].max(), freq="W-MON")
    series = s.set_index("week_start")["units_sold"].reindex(full_idx, fill_value=0)

    train, test = series[:-HOLDOUT_WEEKS], series[-HOLDOUT_WEEKS:]

    model = ExponentialSmoothing(
        train, trend="add", seasonal=None,
        initialization_method="estimated"
    ).fit()
    forecast = model.forecast(HOLDOUT_WEEKS)

    mae = np.mean(np.abs(test.values - forecast.values))
    mape = np.mean(np.abs((test.values - forecast.values) / np.where(test.values == 0, 1, test.values))) * 100

    results.append({
        "StockCode": code, "Description": desc,
        "avg_weekly_units": round(series.mean(), 1),
        "holdout_MAE_units": round(mae, 1),
        "holdout_MAPE_pct": round(mape, 1),
    })

    ax = axes[i]
    ax.plot(train.index, train.values, label="Actual (train)", color="#1F3864")
    ax.plot(test.index, test.values, label="Actual (holdout)", color="#1F3864", linestyle="--")
    ax.plot(test.index, forecast.values, label="Forecast", color="#D9534F")
    ax.set_title(f"{desc[:40]} ({code})", fontsize=9)
    ax.legend(fontsize=7)
    ax.tick_params(axis='x', labelsize=7)

plt.tight_layout()
plt.savefig("../reports/forecast_top5.png", dpi=130)
print("Saved chart to reports/forecast_top5.png")

res_df = pd.DataFrame(results)
res_df.to_csv("../reports/forecast_accuracy.csv", index=False)
print(res_df.to_string(index=False))

conn.close()
