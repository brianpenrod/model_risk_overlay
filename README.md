 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/README.md b/README.md
index 0b44e9caf7dc6d09ce4d94a494e85f97840ee2f4..d268ae6ccb938c0cf87745ae18c4018e59458950 100644
--- a/README.md
+++ b/README.md
@@ -1,2 +1,84 @@
-# BigBs
-my creations
+# Model Risk Governance Overlay (MRGO)
+## Institutional-Grade Controls for High-Frequency Futures Strategies
+
+| **Metric** | **Status** |
+| :--- | :--- |
+| **Model ID** | `BW-NQ-REV-01` |
+| **Asset Class** | Equity Index Futures (CME: NQ/MNQ) |
+| **Risk Tier** | **Tier 2** (Short-Term Tactical / Intraday) |
+| **Validation** | [Passed with Conditions](2_Independent_Validation_Report.md) |
+| **Owner** | Brian Penrod (BPENROD) |
+
+---
+
+## 1. Executive Summary
+This repository houses the **Model Risk Management (MRM)** framework for the **Bud Wiser NQ Reversion** algorithm. Unlike typical retail trading systems that focus solely on entry signals, this framework prioritizes **risk controls, regime detection, and execution governance**.
+
+The system operates on a **"Defensive Alpha"** philosophy:
+> *Alpha is generated not just by selecting the right trade, but by algorithmically rejecting the wrong ones during high-risk regimes.*
+
+---
+
+## 2. Strategy Logic (The "Core Physics")
+The underlying algorithm exploits mean reversion opportunities using **Auction Market Theory** principles.
+
+- **Thesis:** Price probes outside value (ONH/PDH) that fail to find acceptance result in rapid rotation back to the Point of Control (POC).
+- **Signal Construction:**
+  1. **Structural Setup:** "Look Above/Below & Fail" (sweep of reference level).
+  2. **Momentum Confirmation:** 9/21 EMA crossover (1-minute granularity).
+  3. **Execution:** Limit order entry within the "Kill Box" (5 bars post-sweep).
+
+```mermaid
+graph TD
+    %% 1. Data Ingest & Signal Generation
+    A[Live Market Data (1-min NQ)] --> B{Signal Generation}
+    B -->|Logic: Sweep of ONH/PDH| C[Potential Setup]
+    
+    %% 2. The Risk Overlay (Filters)
+    C --> D{Risk Overlay: Filters}
+    D -- "News Event (CPI/NFP +/- 5m)" --> E[BLOCK TRADE]
+    D -- "RSI Extreme (>70 or <30)" --> E
+    D -- "Choppy Regime (<20pt ATR)" --> E
+    
+    %% 3. Confirmation
+    D -- "Filters Passed" --> F{Momentum Confirm}
+    F -- "No 9/21 EMA Cross" --> G[Wait / Decay]
+    
+    %% 4. Execution & Sizing
+    F -- "EMA Cross Confirmed" --> H{Circuit Breaker Status}
+    H -- "Green State" --> I[Execute Full Size]
+    H -- "Amber State (PF < 1.2)" --> J[Execute Half Size]
+    H -- "Red State (DD > 4%)" --> K[KILL SWITCH: NO TRADE]
+    
+    %% 5. Trade Management
+    I & J --> L[Attach Hard Deck Stop]
+    L -->|Stop| M(Swing High/Low + 2 ticks)
+    L -->|Target| N(Fib Extensions 1.272)
+```
+
+---
+
+## 3. Governance Artifacts
+This repository is structured in compliance with **Federal Reserve SR 11-7** (Guidance on Model Risk Management).
+
+| **Artifact** | **Purpose** | **Audience** |
+| :--- | :--- | :--- |
+| Model Development Document (MDD) | Technical specification, feature definitions, and mathematical logic. | Quants / Developers |
+| Independent Validation Report (IVR) | "Red Team" audit findings, stress tests (VIX > 35), and limitations. | Risk Officers |
+| Monitoring Plan | Weekly/Monthly drift checks and "Kill Switch" thresholds. | Operations |
+| Findings Tracker | Live log of identified defects, remediation status, and due dates. | Auditors |
+
+---
+
+## 4. Key Risk Controls
+- **Volmageddon Protection:** Trading is automatically disabled if the 1-hour ATR exceeds 100 points (indicating VIX spike/liquidity crisis).
+- **News Event Lockout:** Hard-coded blackout windows 5 minutes before/after high-impact news (CPI, FOMC, NFP).
+- **Execution Hard Deck:** Stops are placed server-side immediately upon entry (OCO orders) to prevent "runaway algo" losses during disconnects.
+
+---
+
+## 5. Deployment & Versioning
+- **Current State:** Active Monitoring.
+- **Codebase:** Python (Pandas/NumPy for backtesting) → C# (NinjaScript for execution).
+- **Data Source:** Rithmic (tick data) / Topstep (execution venue).
+- **Verified by:** Internal Audit — 2026.
 
EOF
)
