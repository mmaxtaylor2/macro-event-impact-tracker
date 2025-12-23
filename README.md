# Macro Event Impact Tracker

## Overview
The Macro Event Impact Tracker is a Python-based analytical project that measures how major U.S. macroeconomic events impact financial markets. The project replicates a real-world macro research workflow by aligning economic release dates with cross-asset market data and calculating post-event reactions.

The goal is to demonstrate how macroeconomic information (inflation, labor data, and monetary policy decisions) transmits into equity prices, interest rates, and market volatility.

---

## Key Questions
- How do equity markets react to major macroeconomic releases?
- Which events have the largest impact on Treasury yields?
- How does market volatility respond across different event types?

---

## Data Sources
- **Yahoo Finance** – Equity indices, FX proxies, gold, and volatility (VIX)
- **Federal Reserve Economic Data (FRED)** – U.S. Treasury yields
- **Bureau of Labor Statistics (BLS)** – CPI and Non-Farm Payroll event dates
- **Federal Reserve** – FOMC decision dates

All data is historical, publicly available, and programmatically retrieved.

---

## Methodology
1. **Market Data Ingestion**
   - Pulled daily market data across equities, rates, FX, commodities, and volatility
   - Stored clean, reproducible CSV artifacts

2. **Event Calendar Construction**
   - Built a structured macro event calendar for CPI, NFP, and FOMC events

3. **Event Study Framework**
   - Aligned event dates to the nearest trading day
   - Calculated 1-day post-event market reactions
   - Aggregated results by event type

4. **Visualization**
   - Created summary charts illustrating average market reactions
   - Exported static charts for reproducibility and presentation

---

## Key Findings
- **Equities** tend to show the strongest average reactions around inflation and labor market releases.
- **Treasury yields** respond most significantly to Federal Reserve policy decisions.
- **Market volatility (VIX)** increases meaningfully around CPI and FOMC events, reflecting uncertainty around inflation and monetary policy.
- Different macro events transmit through markets in distinct ways, highlighting the importance of event-specific analysis.

---

## Project Structure

=======
>>>>>>> 4a6aeab25acd84c544b7041539372947fa503855

---

## Yield Curve Visualizer & Analytics Engine

This repository also includes a yield curve visualization and analytics engine
that analyzes the U.S. Treasury term structure using both synthetic scenarios
and real market data.

### Features
- Synthetic yield curve scenarios (normal, flat, inverted, steep)
- Live U.S. Treasury yields pulled directly from FRED
- Robust handling of weekends and holidays
- Yield curve comparison across time
- 10Y–2Y spread calculation
- Automatic yield curve regime classification (Normal / Flat / Inverted)

### Outputs
- Static yield curve charts saved to the `/charts` directory
- Terminal analytics summarizing slope and regime classification

This component mirrors how macro and rates analysts monitor interest-rate
conditions and assess recession risk through yield curve dynamics.

