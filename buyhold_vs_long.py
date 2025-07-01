import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV
df = pd.read_csv("QQQ_5min_sample.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)
df.dropna(inplace=True)

# Parameters
capital = 25000
risk_budget = 0.01 * capital  # $250
commission = 0.0005
r_multiple = 10

equity_list = [capital]
time_list = [df.index[0]]
cumulative_pnl = 0

i = 0
while i < len(df) - 1:
    first = df.iloc[i]
    # Long setup only
    entry_price = first['high'] + 0.01
    stop_loss = first['low'] - 0.01
    risk_per_share = entry_price - stop_loss
    shares = int(risk_budget / risk_per_share) if risk_per_share > 0 else 0
    target_price = entry_price + r_multiple * risk_per_share

    position = 0
    entry_time = None
    exit_price = None

    for j in range(i + 1, len(df)):
        high = df.iloc[j]['high']
        low = df.iloc[j]['low']
        close = df.iloc[j]['close']

        if position == 0 and high >= entry_price and shares > 0:
            position = 1
            entry_time = df.index[j]
            continue

        if position == 1:
            if low <= stop_loss:
                exit_price = stop_loss
                exit_time = df.index[j]
                i = j
                break
            elif high >= target_price:
                exit_price = target_price
                exit_time = df.index[j]
                i = j
                break
            elif j == len(df) - 1:
                exit_price = close
                exit_time = df.index[j]
                i = j
                break
    else:
        i += 1
        continue

    if position == 1:
        gross = (exit_price - entry_price) * shares
        fee = shares * commission * 2
        net = gross - fee
        cumulative_pnl += net
        equity_list.append(capital + cumulative_pnl)
        time_list.append(exit_time)
    else:
        i += 1

# Buy and Hold baseline
buy_price = df.iloc[0]['open']
shares_bh = int(capital / buy_price)
cash_left = capital - shares_bh * buy_price
bh_equity = [shares_bh * price + cash_left for price in df['close']]
bh_time = df.index

# Plot both curves
plt.figure(figsize=(12, 6))
plt.plot(time_list, equity_list, marker='o', label='Long-Only Strategy')
plt.plot(bh_time, bh_equity, label='Buy & Hold QQQ', linestyle='--')
plt.title('Buy & Hold vs. Long-Only Strategy Equity Curve')
plt.xlabel('Time')
plt.ylabel('Account Equity ($)')
plt.legend()
plt.grid(True)
plt.show() 