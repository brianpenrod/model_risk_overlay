# Model Monitoring Plan (SOP)
**Model ID:** EMN-QS-2026-V1
**SOP Owner:** Quant Ops Team
**Effective Date:** 2026-02-15

---

## 1. Weekly Checks (Cadence: Every Tuesday 09:00 EST)

### 1.1 Feature Neutral Correlation (FNC)
*   **Metric:** `FNCv4` (Correlation of predictions with target after neutralizing against all features).
*   **Threshold:** Must remain positive (> 0.0).
*   **Logic:** A negative FNC indicates that the "unique alpha" of the model (what isn't explained by simple factors) is actually hurting performance.
*   **Procedure:** Run `check_fnc.py`. If FNC < 0.0 for the current era, flag for review.

### 1.2 Correlation with Metamodel
*   **Metric:** Spearman Correlation with `MetaModel` (Stake-weighted average of all models).
*   **Threshold:** Target range [0.4, 0.8].
*   **Logic:**
    *   < 0.4: Model is too idiosyncratic/risky.
    *   > 0.8: Model provides no diversification benefit.
*   **Procedure:** Check dashboard panel `Similarity_Index`.

---

## 2. Monthly Checks (Cadence: First Friday of Month)

### 2.1 Full Retraining Assessment
*   **Procedure:** Re-train the model with the latest 4 eras of data added.
*   **Check:** Compare Validation IC of the new model vs. the previous month's model.
*   **Pass Condition:** New model Validation IC >= 95% of previous model. If lower, investigate for "concept drift" or bad data in recent eras.

### 2.2 Regime Shift Detection
*   **Method:** Run Hidden Markov Model (HMM) on market volatility and factor return covariance matrix.
*   **Output:** `Prob_Regime_Change` (0 to 1).
*   **Action:** If `Prob_Regime_Change` > 0.7, initiate an ad-hoc meeting with the Risk Committee to discuss potential temporary adjustment of Feature Neutralization parameters.

---

## 3. Triggers & Escalation Matrix

| Status Level | Trigger Condition | Automated Action | Manual Required Action |
| :--- | :--- | :--- | :--- |
| **GREEN** | Rolling 4-week Sharpe > 0.5 AND FNC > 0. | None. | None. |
| **AMBER** | 2 consecutive weeks of negative IC OR FNC < 0. | Send Alert Email to Owner (BPENROD). | **Review Feature Exposure.** Check if a specific feature group (e.g., Momentum) caused the drag. |
| **RED** | Rolling 4-week Sharpe < 0.0. | **Halve Stay/Position Size.** | **Disable Model Slot.** Conduct full "post-mortem" analysis before re-enabling. |
