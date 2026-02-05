# Model Development Document (MDD)
**Model Name:** Equity Market Neutral Quantitative Strategy (EMN-QS)
**Model ID:** EMN-QS-2026-V1
**Document Version:** 1.0
**Date:** 2026-02-05

---

## 1. Executive Summary
**Objective:**
The primary objective of the EMN-QS model is to generate alpha (excess returns independent of broad market movements) by predicting the relative performance of a universe of global equities. The model aims to maximize the **Information Coefficient (IC)**—defined as the Spearman rank correlation between the model's predictions and the subsequent era's realized returns—while strictly minimizing exposure to identified risk factors and feature clusters.

**Key Goals:**
*   Achieve a mean validation IC > 0.02.
*   Maintain feature exposure < 0.05 post-neutralization.
*   Operate within a strict market-neutral framework (0 beta to major indices).

**Model Tier:**
Tier 1 (Critical) - Used for direct capital allocation.

---

## 2. Data Lineage

### 2.1 Data Sources
*   **Primary Source:** Obfuscated and regularized financial data provided by the specific data vendor (e.g., Numerai). 
*   **Data Type:** Tabular data representing fundamental, technical, and alternative signals. All features are anonymized to prevent bias and ensure privacy.
*   **Granularity:** Era-based (weekly frequencies).

### 2.2 Preprocessing
*   **Winsorization:** Outliers are clipped at the 1st and 99th percentiles to reduce the impact of extreme values.
*   **Era-wise Standardization:** All features are standardized within each era (time-step) to defined ranges (e.g., [0, 1] or integer bins) to ensure stationarity across potential regime shifts. The target variable is also rank-standardized per era.
*   **Data Integrity Checks:** Null values are handled via imputation (median of the era) or dropped if exceeding 5% of the row data.

### 2.3 Train/Val/Test Splits
*   **Training Set:** Eras 1 through 500 (Historical Regime).
*   **Validation Set:** Eras 501 through 600 (Recent/OOS Proxy). Used for hyperparameter tuning and early stopping.
*   **Test Set:** Eras 601+ (Strictly held-out for final IVR assessment).
*   **Embargo:** An embargo period of 4 eras is applied between Train and Validation to prevent leakage due to the overlapping nature of the target labels.

---

## 3. Feature Set

### 3.1 Feature Groups
Features are organized into conceptual groups to aid in neutralization strategies:
*   **Group A (Momentum-proxy):** High autocorrelation features.
*   **Group B (Value-proxy):** Fundamental ratio proxies.
*   **Group C (Volatility-proxy):** Price variance and range proxies.
*   **Group D (Sentiment/Alternative):** Non-price derived signals.

### 3.2 Correlation Clusters
Hierarchical clustering is performed to identify redundant features.
*   **Selection Logic:** We utilize **Feature Importance (via Permutation Importance)** penalized by **Downside Deviation**.
*   **Reduction:** If two features exhibit a correlation > 0.95, the feature with the lower Sharpe contribution in the training set is dropped to reduce dimensionality and noise.

---

## 4. Methodology

### 4.1 Architecture
*   **Core Algorithm:** Gradient Boosted Decision Trees (GBDT) using **XGBoost** (Extreme Gradient Boosting).
*   **Rationale:** GBDTs provide superior handling of non-linear interactions between obfuscated features compared to linear models, and offer better interpretability than deep neural networks for this specific tabular dataset.

### 4.2 Loss Functions
*   **Primary Loss:** **Correlation Loss** (1 - Spearman Correlation). We optimize directly for rank correlation rather than Mean Squared Error (MSE), as the magnitude of returns is less relevant than the relative ordering of assets.
*   **Auxiliary Loss:** A custom "Sharpe Component" loss is added to penalize variance in era-wise predictions.

### 4.3 Hyperparameter Optimization
*   **Strategy:** **Bayesian Optimization** (using Tree-structured Parzen Estimator - TPE) is preferred over Grid Search for efficiency.
*   **Search Space:**
    *   `max_depth`: [4, 10]
    *   `learning_rate`: [0.001, 0.05]
    *   `colsample_bytree`: [0.1, 0.8] (Crucial for preventing overfitting to specific feature groups)
    *   `subsample`: [0.5, 0.9]

---

## 5. Neutralization

To mitigate non-stationarity and regime risk, we apply **Feature Neutralization (FN)** to the raw model predictions.

### 5.1 Definition
*   **Mechanism:** We regress the model's raw predictions against a set of features (or feature clusters) and subtract the linear component explained by those features.
    $$ \hat{Y}_{neutral} = \hat{Y}_{raw} - \beta \cdot F $$
    Where $F$ is the matrix of features to be neutralized against.

### 5.2 Proportion Applied
*   **Standard Setting:** 50% Feature Neutralization.
    *   This strikes a balance between retaining the alpha signal (which may partially reside in the feature exposure) and protecting against "feature blow-ups" (regimes where specific factors underperform strictly).
*   **Maximum Exposure Constraint:** No single feature group shall explain more than 5% of the variance of the final prediction vector.

---

## 6. Limitations

*   **Execution Lag:** The model assumes instantaneous execution at the closing price of the era. Real-world slippage and liquidity constraints are not modeled in the raw alpha generation but are handled by the downstream Trade Execution Engine.
*   **Short-side Availability:** The theoretical mapping assumes the ability to short any asset in the universe. In practice, borrow costs and hard-to-borrow lists may constrain the realization of the short leg of the portfolio.
*   **Non-Stationarity:** While feature neutralization mitigates regime risk, extreme "black swan" events (e.g., market-wide freezes) that differ structurally from all training eras remain a residual risk. The model assumes a degree of continuity in the covariance structure of returns.
