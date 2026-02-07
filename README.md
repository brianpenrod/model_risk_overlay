# Quantitative Risk Overlay & Allocation Engine
### Automated Fiduciary Controls for Multi-Model Portfolios

[![Risk Grade](https://img.shields.io/badge/Risk_Class-Institutional-blue)]()
[![Compliance](https://img.shields.io/badge/Compliance-SR_11--7-green)]()
[![Status](https://img.shields.io/badge/Status-Active_Monitoring-success)]()

> **Author:** **Brian Penrod, DBA**
> *Retired US Army Special Forces CSM | Doctor of Business Administration (Finance)*

---

## 📉 Business Scenario & Objective

In institutional portfolio management, **Alpha Generation** and **Risk Management** must be decoupled to prevent conflict of interest. While the Alpha models (Operation Overwatch) seek to maximize returns, this **Risk Overlay** acts as the "Second Line of Defense."

**The Business Mandate:**
1.  **Volatility Targeting:** Maintain an annualized portfolio volatility of **15%**, regardless of market conditions.
2.  **Correlation Guard:** Automatically detect when "Market Neutral" models begin to correlate (Systemic convergence) and reduce exposure dynamically.
3.  **Drawdown Control:** Enforce a hard "De-grossing" protocol if drawdown limits are breached.

---

## 🏗 System Architecture

The Risk Overlay sits downstream from the Signal Generation engine. It acts as a **Gatekeeper** before any order is sent to the exchange.



### Core Modules

1.  **`volatility_estimator.py`**:
    * Calculates 20-day and 60-day rolling realized volatility for each strategy.
    * *Logic:* If realized vol spikes, position size is mathematically reduced to maintain the 15% target (Inverse Volatility Sizing).

2.  **`correlation_matrix.py`**:
    * Monitors the pairwise correlation between `KZ_CORE`, `KZ_BAL`, and `KZ_DEF`.
    * *Circuit Breaker:* If pairwise correlation > 0.90 (indicating a liquidity crisis where "all correlations go to 1"), the system cuts leverage by 50%.

3.  **`allocation_optimizer.py`**:
    * Uses **Hierarchical Risk Parity (HRP)** to allocate capital. Unlike Mean-Variance optimization (which chases past returns), HRP allocates based purely on the risk structure of the cluster.

---

## 📊 Operational Logic (The "De-Grossing" Algorithm)

The system follows a strict logical flow to determine the final `Capital_Allocation_Vector`:

```mermaid
graph TD
    A[Raw Model Signals] --> B{Volatility Check}
    B -->|Vol < 15%| C{Correlation Check}
    B -->|Vol > 15%| D["Reduce Leverage (Scalar < 1.0)"]
    D --> C
    
    C -->|Corr < 0.8| E[Allocate via Risk Parity]
    C -->|Corr > 0.8| F["Trigger Circuit Breaker (-50% Size)"]
    
    E & F --> G[Final Execution Orders]
 ```

🛡️ Governance & Compliance
This repository adheres to Federal Reserve Guidance SR 11-7 (Model Risk Management) by establishing:

Input Validation: Strict type-checking of return streams.

Limit Monitoring: Hard-coded limits in risk_policy.yaml that cannot be overridden by the trading algorithm.

Audit Trail: Every allocation decision is logged with a timestamp and the specific risk metric that triggered it (e.g., "Leverage reduced due to Volatility Spike on 2026-02-07").

🚀 Usage
# Run the daily risk assessment
python run_risk_overlay.py --portfolio "kinetic_zero_live" --config "risk_policy.yaml"
Output Artifacts
risk_report_YYYY-MM-DD.pdf: Executive summary of current exposures.

target_weights.csv: The approved capital allocation for the next trading session.

🔒 Access & IP
This module represents proprietary risk management logic. Source code available for review upon request.
---

