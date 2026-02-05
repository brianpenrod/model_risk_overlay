# Model Development Document (MDD)
**Model ID:** BW-NQ-REV-01 (Bud Wiser NQ Reversion)
**Owner:** Brian Penrod (BPENROD)
**Version:** 1.0

## 1. Executive Summary
This model algorithmically captures mean reversion opportunities in Nasdaq-100 Futures (NQ/MNQ) based on Auction Market Theory. The primary objective is to identify "Look Above/Below & Fail" events where price probes critical reference levels (ONH, PDH, VAH/VAL) but fails to sustain acceptance, signaling a rotation back to value. The model utilizes 1-minute granularity for trigger validation (9/21 EMA crosses) to minimize drawdown duration.

## 2. Data Lineage
* **Primary Source:** CME Group Level 2 Data (via Rithmic/Topstep).
* **Frequency:** 1-minute OHLCV (Open, High, Low, Close, Volume).
* **Key Reference Levels (Calculated Daily):**
    * *ONH/ONL:* Overnight High/Low (GlobeX session).
    * *PDH/PDL:* Prior Day High/Low (RTH session).
    * *VAH/VAL:* Value Area High/Low (70% TPO profile).
    * *POC:* Point of Control.

## 3. Feature Set
The model relies on interaction features between Price ($P_t$) and Reference Levels ($L_{ref}$).

### 3.1 Failed Auction Feature (The "Sweep")
A "Sweep and Fail" event at time $t$ is defined as a Boolean feature $F_{sweep}$:

$$
F_{sweep, t} = 
\begin{cases} 
1 & \text{if } (H_t > L_{ref}) \land (C_t < L_{ref}) \quad \text{[Bearish Look Above & Fail]} \\
1 & \text{if } (L_t < L_{ref}) \land (C_t > L_{ref}) \quad \text{[Bullish Look Below & Fail]} \\
0 & \text{otherwise}
\end{cases}
$$

Where $L_{ref} \in \{ONH, PDH, VAH, VAL\}$.

### 3.2 Momentum Confirmation (EMA Cross)
To filter false positives, the model requires a momentum shift defined by the 9-period and 21-period Exponential Moving Averages (EMA):

$$
F_{cross, t} = 
\begin{cases} 
1 & \text{if } (EMA_{9,t-1} > EMA_{21,t-1}) \land (EMA_{9,t} < EMA_{21,t}) \quad \text{[Bearish Cross]} \\
1 & \text{if } (EMA_{9,t-1} < EMA_{21,t-1}) \land (EMA_{9,t} > EMA_{21,t}) \quad \text{[Bullish Cross]} \\
0 & \text{otherwise}
\end{cases}
$$

## 4. Methodology
The trading signal ($S_t$) is generated only when structural location and momentum confirmation align within a specific temporal window.

### 4.1 Entry Logic
The algorithm enters a position when a Sweep is followed by a Cross within $k$ bars (default $k=5$):

$$
S_{entry} = \exists k \in [0, 5] : (F_{sweep, t-k} = 1) \land (F_{cross, t} = 1) \land (RSI_{14} \notin \text{Extreme})
$$

### 4.2 Risk Management (The "Hard Deck")
* **Stop Loss:** Placed rigidly at the swing high/low of the sweep candle ($H_{sweep}$ or $L_{sweep}$) plus 2 ticks.
* **Take Profit:** Dynamic targets based on Fibonacci extensions (1.272, 1.618) of the impulse leg.

## 5. Neutralization & Risk Controls
* **News Filter:** Model logic is disabled 5 minutes pre/post High Impact News (CPI, FOMC, NFP).
* **Regime Filter:** Long-only logic applied if Price > 5-Day VWAP; Short-only if Price < 5-Day VWAP (Trend Pullback Mode).

## 6. Limitations
* **Choppiness:** In balanced profiles (Gaussian distribution width < 0.5% ATR), EMA crosses produce higher false positive rates.
* **Execution Lag:** 1-minute trigger assumes fill at $C_t$; slippage in fast markets (NFP) is not modeled in theoretical backtests.
