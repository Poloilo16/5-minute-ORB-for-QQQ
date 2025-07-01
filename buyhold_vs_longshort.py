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
    # Long setup
    long_entry_price = first['high'] + 0.01
    long_stop_loss = first['low'] - 0.01
    long_risk_per_share = long_entry_price - long_stop_loss
    long_shares = int(risk_budget / long_risk_per_share) if long_risk_per_share > 0 else 0
    long_target_price = long_entry_price + r_multiple * long_risk_per_share

    # Short setup
    short_entry_price = first['low'] - 0.01
    short_stop_loss = first['high'] + 0.01
    short_risk_per_share = short_stop_loss - short_entry_price
    short_shares = int(risk_budget / short_risk_per_share) if short_risk_per_share > 0 else 0
    short_target_price = short_entry_price - r_multiple * short_risk_per_share

    position = 0  # 0 = no position, 1 = long, -1 = short
    entry_time = None
    exit_price = None

    for j in range(i + 1, len(df)):
        high = df.iloc[j]['high']
        low = df.iloc[j]['low']
        close = df.iloc[j]['close']

        # Check for long entry
        if position == 0 and high >= long_entry_price and long_shares > 0:
            position = 1
            shares = long_shares
            entry_price = long_entry_price
            stop_loss = long_stop_loss
            target_price = long_target_price
            entry_time = df.index[j]
            continue

        # Check for short entry
        if position == 0 and low <= short_entry_price and short_shares > 0:
            position = -1
            shares = short_shares
            entry_price = short_entry_price
            stop_loss = short_stop_loss
            target_price = short_target_price
            entry_time = df.index[j]
            continue

        # Manage long position
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

        # Manage short position
        if position == -1:
            if high >= stop_loss:
                exit_price = stop_loss
                exit_time = df.index[j]
                i = j
                break
            elif low <= target_price:
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

    # Results
    if position == 1:  # Long
        gross = (exit_price - entry_price) * shares
    elif position == -1:  # Short
        gross = (entry_price - exit_price) * shares
    else:
        gross = 0

    if position != 0:
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
plt.plot(time_list, equity_list, marker='o', label='Long & Short Strategy')
plt.plot(bh_time, bh_equity, label='Buy & Hold QQQ', linestyle='--')
plt.title('Buy & Hold vs. Long & Short Strategy Equity Curve')
plt.xlabel('Time')
plt.ylabel('Account Equity ($)')
plt.legend()
plt.grid(True)
plt.show() 