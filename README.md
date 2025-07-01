# 5-minute-ORB-for-QQQ
This repository implements an Opening Range Breakout (ORB) strategy for QQQ ETF using historical intraday data from the 17th of June 2025 to the 1st of July 2025. The strategy is designed to capture directional momentum shortly after market open by trading breakouts from the first 5-minute range. It's supposed to be a replication of the results from Carlo Zarattini and Andrew Aziz paper "can day trading really be profitable". Unlike Zarattini and Andrew Aziz, I decided to compare two strategies (1) only calling QQQ (2) calling and shorting QQQ. 

---

## Strategy Logic

1. **Opening Range Definition**:
   - The opening range is defined as the **first 5 minutes** of the trading day (09:30–09:35).
   - We record the **high and low** of this range.

2. **Entry Rule**:
   - If price **breaks above the opening range high**, we enter a **long** position.
   - if price **breaks below the openeing range low**, we wnter a **short** position

3. **Stop-Loss and Target**:
   - **Stop-Loss** = Opening range low
   - **$R** = Entry price – Stop price
   - **Target Price** = Entry price + **10 × $R**

4. **Exit Rule**:
   - If the price reaches the profit target during the day, exit at the target.
   - If the target is not hit, exit at **end-of-day (EoD)** market close.
     
---

## Position Sizing

We risk **1% of capital per trade**, following the formula:
Shares = int[min( (A × 0.01)/$R , (4 × A)/P )]
Where:
- `A` = Account equity
- `$R` = Risk per share = Entry – Stop
- `P` = Entry price
- The left term caps based on **risk**, and the right term caps based on **leverage (4×)**

## Assumptions

- **Starting Capital**: $25,000
- **Max Leverage**: 4×
- **Commission**: $0.0005 per share (entry and exit)
- **Risk per Trade**: 1% of capital
- **Target**: 10× the risk amount ($R)

## Results Summary 

The backtest results show that the **Long-Only ORB strategy** delivered the highest equity growth, outperforming both the **Buy & Hold QQQ** approach and the **Long & Short ORB variant**.

- The **Long-Only strategy** performed best in capturing upside breakouts during bullish momentum.
- The **Buy & Hold** portfolio showed steady gains, benefiting from QQQ's long-term upward bias.
- The **Long & Short strategy**, while more dynamic, underperformed due to whipsaws and short-side losses during choppy or upward-trending sessions.

These results suggest that in the tested period, directional simplicity (long-only) offered more consistent returns than adding short exposure, at least within the ORB framework.

## Limitations

- **No Slippage or Fill Delay**: Assumes perfect execution at breakout, stop, or target levels, which may not reflect real-world trading conditions.
- **No Overnight Risk**: Positions are closed by end-of-day; the model ignores potential overnight gaps or multi-day holding opportunities.
- **No Trade Filtering**: All breakouts are treated equally; no confirmation via volume, trend, or volatility filters is applied.
- **Fixed Parameters**: Profit target is set at 10× risk for all trades; results could vary with dynamic target sizing or trailing exits.
- **Limited Backtest Horizon**: Short testing window may not fully capture broader market cycles or structural shifts.
