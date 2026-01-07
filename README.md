## Macro Event Impact Tracker

A Python-based analytical project that measures how major U.S. macroeconomic events transmit into financial markets. The project replicates a macro research workflow by aligning economic release dates with cross-asset market data and evaluating post-event reactions across equities, interest rates, and volatility.

The goal is to demonstrate how inflation data, labor market releases, and monetary policy decisions affect market pricing and risk sentiment.

## Problem Context

Macroeconomic events are often discussed qualitatively, but isolating their market impact requires a structured event-study framework. This project was built to systematically measure how different types of U.S. macro releases affect asset prices and yields, enabling consistent comparison across events and asset classes.

## Key Questions

- How do equity markets react to major U.S. macroeconomic releases?
- Which events have the largest impact on Treasury yields?
- How does market volatility respond across different event types?

## Data Sources

- Yahoo Finance – Equity indices, FX proxies, commodities, and volatility (VIX)
- Federal Reserve Economic Data (FRED) – U.S. Treasury yields
- Bureau of Labor Statistics (BLS) – CPI and Non-Farm Payroll release dates
- Federal Reserve – FOMC decision dates

All data is historical, publicly available, and programmatically retrieved.

## Methodology

### Market Data Ingestion
- Pulled daily market data across equities, rates, FX, commodities, and volatility
- Stored clean, reproducible CSV artifacts

### Event Calendar Construction
- Built a structured macro event calendar for CPI, NFP, and FOMC events
- Standardized event labeling and timestamps

### Event Study Framework
- Aligned event dates to the nearest trading day
- Calculated one-day post-event market reactions
- Aggregated results by event type

### Visualization
- Created summary charts illustrating average market reactions
- Exported static figures for reproducibility and presentation

## Outputs and Artifacts

This project generates multiple static charts by design. Each figure corresponds to a specific macro event study, asset class, or yield curve scenario and is saved as a standalone artifact to support reproducibility, comparison across runs, and offline review.

## Key Findings

- Equity markets exhibit the strongest average reactions around inflation and labor market releases
- Treasury yields respond most significantly to Federal Reserve policy decisions
- Market volatility increases meaningfully around CPI and FOMC events, reflecting policy and inflation uncertainty
- Different macro events transmit through markets in distinct ways, underscoring the importance of event-specific analysis

## Yield Curve Analytics Engine

This repository also includes a yield curve visualization and analytics engine designed to monitor U.S. Treasury term structure dynamics under both real and simulated scenarios.

### Features

- Synthetic yield curve scenarios (normal, flat, inverted, steep)
- Live U.S. Treasury yields pulled from FRED
- Robust handling of weekends and holidays
- Yield curve comparison across time
- 10Y–2Y spread calculation
- Automatic regime classification (Normal / Flat / Inverted)

### Outputs

- Static yield curve charts saved to the `/charts` directory
- Terminal-based analytics summarizing curve slope and regime classification

This component mirrors how macro and rates analysts monitor interest-rate conditions and assess recession risk through yield curve behavior.

## Scope Note

This project is intended for analytical demonstration and portfolio use and is not a trading or investment system.
