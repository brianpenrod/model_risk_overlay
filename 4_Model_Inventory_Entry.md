# Model Inventory Entry
**Status:** ACTIVE

| Field | Value | Notes |
| :--- | :--- | :--- |
| **Model_ID** | `EMN-QS-2026-V1` | Unique identifier. |
| **Model Name** | Equity Market Neutral Quantitative Strategy | |
| **Owner** | `BPENROD` | Head of Quant Research. |
| **Developer** | `AI_AGENT_007` | |
| **Risk_Tier** | **Tier 1 - Critical** | Direct impact on P&L. |
| **Validation_Cycle** | Annual | Next Review: Feb 2027. |
| **Business Unit** | Equities Trading | |
| **Use Case** | Alpha Signal Generation | Predicts relative stock performance. |
| **Downstream Dependencies** | **Trade Execution Engine** | Feeds directly into the portfolio optimizer. |
| **Upstream Dependencies** | `Numerai_Data_API` | Relying on v4.2 dataset release. |
| **Key Controls** | Pre-submission Feature Neutralization Check | Hard stop if predicted feature exposure > 0.1. |
| **Technology Stack** | Python 3.9, XGBoost 1.7, Pandas 1.5 | |
| **Model Type** | Machine Learning (Non-deterministic) | Gradient Boosted Decision Trees. |
| **Approval Date** | 2026-02-05 | Approved by Model Risk Committee. |
