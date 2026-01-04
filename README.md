# Long Straddle on SPY — Delta Hedging and Execution Risk

This repository contains an academic project analyzing a **long straddle strategy on SPY options**, combining option theory, quantitative simulation, and execution risk analysis.

The project was developed as part of a graduate-level program focused on financial markets and quantitative methods.

---

## Project Objectives

The main goals of this project are:
- To analyze the payoff and risk profile of a long straddle strategy.
- To study delta hedging under the Black–Scholes framework.
- To quantify **execution (legging) risk** when entering multi-leg option strategies.

---

## Methodology Overview

### Option Chain and Contracts
- Option chains are retrieved via the Interactive Brokers API.
- Monthly expirations and ATM strikes are selected.
- Contracts are qualified using IBKR identifiers (`conId`).

### Pricing and Greeks
- Option prices and deltas are computed using the Black–Scholes model.
- The `py_vollib` library is used for numerically stable pricing and greek calculations.

### P&L Simulation
- Unhedged straddle payoffs are simulated under a geometric Brownian motion.
- A delta-hedged straddle is implemented with daily rebalancing to isolate gamma effects.

### Execution (Legging) Risk
- Execution delays between option legs are simulated over short time windows (0–20 seconds).
- Robust tail metrics (quantiles) are used instead of raw maxima.
- Results show that execution risk does not alter expected P&L but degrades the risk profile by increasing dispersion and reducing effective convexity.

---

## Key Findings

- Long straddles exhibit strong convexity and positive gamma exposure.
- Delta hedging neutralizes directional risk and produces near-zero expected P&L under Black–Scholes assumptions.
- Execution delays increase entry price uncertainty and worsen downside tail outcomes.
- Legging risk is an operational risk distinct from market risk and materially affects multi-leg option strategies.

---

## Limitations

- The Interactive Brokers paper trading account does not provide live or delayed option market data.
- Pricing and hedging rely on model-based assumptions rather than real market quotes.
- The codebase is prepared to integrate real market data if access is enabled.

---

## Disclaimer

This project is for educational purposes only and does not constitute financial or investment advice.
