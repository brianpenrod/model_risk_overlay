# Model Monitoring Plan
**Model ID:** BW-NQ-REV-01
**Review Cycle:** Weekly (Friday Close)

## 1. Weekly Performance Checks
Every Friday at 16:15 EST, the following metrics are calculated for the trailing week:

### A. Performance Decay
* **Metric:** Realized Profit Factor (PF).
* **Threshold:** Must be > 1.20 over a rolling 5-day period.
* **Action:** If PF < 1.20, initiate "Amber State" (Review trade logs for execution errors).

### B. Drift Detection (The "Vibe Check")
We monitor if the market structure has shifted away from the model's training assumptions.
* **Metric:** Average True Range (ATR-14) on 1-hour chart.
* **Threshold:**
    * *Low Vol Limit:* ATR < 20 points (Market is too dead for reversal targets).
    * *High Vol Limit:* ATR > 100 points (Market is too violent for 1-minute stops).
* **Action:** If ATR breaches limits, reduce position size by 50% until normalization.

## 2. Monthly Deep Dive
Performed on the last trading day of the month.
* **Retraining Assessment:** Run the strategy on the most recent month's data. If the *Information Coefficient (IC)* between signal and return is < 0.01, the parameters (EMA lengths) must be re-optimized.
* **Broker Audit:** Compare "Strategy Theoretical Entry" vs. "Broker Realized Entry." If average slippage > 1.5 ticks/trade, switch order routing or execution algo.

## 3. Triggers & Circuit Breakers

| Status | Trigger Condition | Required Action |
| :--- | :--- | :--- |
| **GREEN** | PF > 1.5, Drawdown < 2% | Full Risk Allocation (100%) |
| **AMBER** | PF < 1.2 *OR* 2 Consecutive Losing Days | **Half Risk:** Cut sizing to 50%. Review daily logs. |
| **RED** | Max Drawdown > 4% *OR* 4 Consecutive Losing Days | **KILL SWITCH:** Disable model. Revert to paper trading. |

## 4. Rollback Protocol
If a "Red State" is triggered:
1.  Close all active positions immediately.
2.  Disable the specific strategy in the execution platform (Rithmic/NinjaTrader).
3.  Tag the Model Version as "DEPRECATED" in GitHub.
4.  Revert to the previous stable version (e.g., v1.0) if available.
