# event_study.py
# Purpose: Measure 1-day market reactions to macro events
# Focus: CPI / FOMC / NFP
# Asset focus: 2Y Treasury yield (rates response)

import os
import pandas as pd
from fredapi import Fred

# -----------------------------
# FRED API connection
# -----------------------------

FRED_API_KEY = "2839b1e8d1d2a3585ee14984a24b0805"
fred = Fred(api_key=FRED_API_KEY)

# -----------------------------
# Load 2Y Treasury yield data
# -----------------------------

def load_2y_yield(start_date="2015-01-01"):
    series = fred.get_series("DGS2", observation_start=start_date)

    df = series.reset_index()
    df.columns = ["date", "ust_2y"]
    df["date"] = pd.to_datetime(df["date"])
    df = df.dropna()

    return df

# -----------------------------
# Load macro event dates
# -----------------------------

def load_macro_events(filepath="data/macro_events.csv"):
    df = pd.read_csv(filepath)
    df["event_date"] = pd.to_datetime(df["event_date"])
    return df

# -----------------------------
# Compute 1-day reaction
# -----------------------------

def compute_1d_reaction(events_df, rates_df):
    results = []

    for _, row in events_df.iterrows():
        event_date = row["event_date"]
        event_type = row["event_type"]
        event_id = row["event_id"]

        pre = rates_df[rates_df["date"] <= event_date].iloc[-1:]
        post = rates_df[rates_df["date"] > event_date].iloc[:1]

        if pre.empty or post.empty:
            continue

        reaction_bps = (post["ust_2y"].values[0] - pre["ust_2y"].values[0]) * 100

        results.append({
            "event_id": event_id,
            "event_type": event_type,
            "event_date": event_date,
            "ust_2y_bps_1d": reaction_bps
        })

    return pd.DataFrame(results)

# -----------------------------
# Optional: Load existing reactions
# -----------------------------

def load_event_reactions(filepath="outputs/event_reaction_1d.csv"):
    df = pd.read_csv(filepath)
    df["event_date"] = pd.to_datetime(df["event_date"])
    return df

def filter_cpi_2y_reactions(df):
    cpi_df = df[df["event_type"] == "CPI"].copy()
    return cpi_df[["event_id", "event_date", "ust_2y_bps_1d"]]

# -----------------------------
# MAIN RUNNER (ALWAYS LAST)
# -----------------------------

if __name__ == "__main__":
    print(">>> Running macro event reaction study <<<")

    rates = load_2y_yield()
    events = load_macro_events()

    reaction_df = compute_1d_reaction(events, rates)

    os.makedirs("outputs", exist_ok=True)
    output_path = "outputs/event_reaction_1d.csv"
    reaction_df.to_csv(output_path, index=False)

    print(f">>> Saved output to {output_path}")
    print(reaction_df.head())

    summarize_cpi_reactions(output_path)

    # -----------------------------
# CPI normalization helper
# -----------------------------

def summarize_cpi_reactions(filepath="outputs/event_reaction_1d.csv"):
    """
    Computes average 1-day 2Y Treasury reaction to CPI releases.
    """
    df = pd.read_csv(filepath)
    df["event_date"] = pd.to_datetime(df["event_date"])

    cpi_df = df[df["event_type"] == "CPI"]

    avg_reaction = cpi_df["ust_2y_bps_1d"].mean()
    std_reaction = cpi_df["ust_2y_bps_1d"].std()

    print(">>> CPI 1-Day 2Y Reaction Summary <<<")
    print(f"Average reaction (bps): {avg_reaction:.2f}")
    print(f"Std dev (bps): {std_reaction:.2f}")

    return cpi_df