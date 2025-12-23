"""
Yield Curve Visualizer & Analytics Engine

Description:
- Generates synthetic yield curve scenarios (normal, flat, inverted, steep)
- Pulls real U.S. Treasury yields from FRED
- Handles weekends/holidays robustly
- Visualizes curve shifts over time
- Computes 10Y–2Y slope and regime classification

Outputs:
- Saved PNG charts in /charts
- Terminal analytics summary

Author: Max Taylor
"""


import os
import pandas as pd
import matplotlib.pyplot as plt

print("SCRIPT STARTED")

# --------------------------------------------------
# Project paths
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHART_DIR = os.path.join(BASE_DIR, "charts")
os.makedirs(CHART_DIR, exist_ok=True)

print("Charts directory:", CHART_DIR)

# --------------------------------------------------
# Common maturities
# --------------------------------------------------
maturities = [0.25, 0.5, 1, 2, 5, 10, 20, 30]

# --------------------------------------------------
# Yield curve scenarios
# --------------------------------------------------
yield_scenarios = {
    "normal":   [5.30, 5.20, 5.05, 4.80, 4.40, 4.20, 4.35, 4.40],
    "flat":     [4.80, 4.78, 4.75, 4.72, 4.70, 4.68, 4.67, 4.66],
    "inverted": [5.40, 5.30, 5.10, 4.70, 4.30, 4.10, 4.15, 4.20],
    "steep":    [3.80, 3.90, 4.10, 4.50, 5.00, 5.40, 5.60, 5.70],
}

# --------------------------------------------------
# Generate and save plots
# --------------------------------------------------
for scenario, yields in yield_scenarios.items():
    print(f"Plotting scenario: {scenario}")

    df = pd.DataFrame({
        "Maturity (Years)": maturities,
        "Yield (%)": yields
    })

    plt.figure()
    plt.plot(df["Maturity (Years)"], df["Yield (%)"], marker="o")
    plt.xlabel("Maturity (Years)")
    plt.ylabel("Yield (%)")
    plt.title(f"Yield Curve Scenario: {scenario.capitalize()}")
    plt.grid(True)

    output_path = os.path.join(CHART_DIR, f"yield_curve_{scenario}.png")
    plt.savefig(output_path)
    plt.close()

    print(f"Saved -> {output_path}")

print("SCRIPT FINISHED")


# ==================================================
# PHASE A: REAL TREASURY DATA FROM FRED
# ==================================================

from fredapi import Fred
from datetime import datetime, timedelta

print("\nSTARTING PHASE A: FRED DATA")

# ----------------------------------
# Initialize FRED
# ----------------------------------
FRED_API_KEY = "2839b1e8d1d2a3585ee14984a24b0805"
fred = Fred(api_key=FRED_API_KEY)

# ----------------------------------
# Treasury series (constant maturity)
# ----------------------------------
fred_series = {
    "3M": "DTB3",
    "2Y": "DGS2",
    "5Y": "DGS5",
    "10Y": "DGS10",
    "30Y": "DGS30",
}

maturity_years = {
    "3M": 0.25,
    "2Y": 2,
    "5Y": 5,
    "10Y": 10,
    "30Y": 30,
}

# ----------------------------------
# Helper function (ROBUST)
# ----------------------------------
def fetch_yield_curve(date, label):
    yields = []

    for tenor, series_id in fred_series.items():
        data = fred.get_series(
            series_id,
            observation_start=date - timedelta(days=10),
            observation_end=date
        ).dropna()

        if data.empty:
            raise ValueError(f"No data returned for {series_id}")

        yields.append(data.iloc[-1])

    df = pd.DataFrame({
        "Maturity (Years)": [maturity_years[k] for k in fred_series.keys()],
        "Yield (%)": yields
    })

    plt.figure()
    plt.plot(df["Maturity (Years)"], df["Yield (%)"], marker="o")
    plt.xlabel("Maturity (Years)")
    plt.ylabel("Yield (%)")
    plt.title(f"U.S. Treasury Yield Curve ({label})")
    plt.grid(True)

    output_path = os.path.join(CHART_DIR, f"yield_curve_fred_{label}.png")
    plt.savefig(output_path)
    plt.close()

    print(f"Saved FRED curve -> {output_path}")

    return df

# ----------------------------------
# Dates
# ----------------------------------
today = datetime.today()
one_year_ago = today - timedelta(days=365)

# ----------------------------------
# Generate curves
# ----------------------------------
df_latest = fetch_yield_curve(today, "latest")
df_1y = fetch_yield_curve(one_year_ago, "1y_ago")

# ----------------------------------
# Comparison plot
# ----------------------------------
plt.figure()
plt.plot(df_latest["Maturity (Years)"], df_latest["Yield (%)"], marker="o", label="Latest")
plt.plot(df_1y["Maturity (Years)"], df_1y["Yield (%)"], marker="o", label="1 Year Ago")
plt.xlabel("Maturity (Years)")
plt.ylabel("Yield (%)")
plt.title("U.S. Treasury Yield Curve Comparison")
plt.legend()
plt.grid(True)

comparison_path = os.path.join(CHART_DIR, "yield_curve_fred_comparison.png")
plt.savefig(comparison_path)
plt.close()

print(f"Saved comparison -> {comparison_path}")
print("PHASE A COMPLETE")

# ==================================================
# PHASE B: YIELD CURVE ANALYTICS
# ==================================================

print("\nSTARTING PHASE B: YIELD CURVE ANALYTICS")

# Extract key maturities
yield_2y = df_latest.loc[df_latest["Maturity (Years)"] == 2, "Yield (%)"].iloc[0]
yield_10y = df_latest.loc[df_latest["Maturity (Years)"] == 10, "Yield (%)"].iloc[0]

# Compute slope
slope_10y_2y = yield_10y - yield_2y

# Inversion logic
is_inverted = slope_10y_2y < 0

# Regime classification
if slope_10y_2y < -0.25:
    regime = "Inverted"
elif slope_10y_2y < 0:
    regime = "Flat"
else:
    regime = "Normal"

print("Yield Curve Analytics (Latest)")
print(f"10Y–2Y Spread: {slope_10y_2y:.2f}%")
print(f"Inverted: {is_inverted}")
print(f"Regime: {regime}")

print("PHASE B COMPLETE")

