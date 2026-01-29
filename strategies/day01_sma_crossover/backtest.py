import pandas as pd
import matplotlib.pyplot as plt

from utils.data_loader import load_price_data
from utils.indicators import sma


# 1. Load data
df = load_price_data("ETERNAL.NS", start="2022-01-01")

# 2. Indicators
df["sma_20"] = sma(df["close"], 20)
df["sma_50"] = sma(df["close"], 50)

# 3. Signals
df["signal"] = 0
df.loc[df["sma_20"] > df["sma_50"], "signal"] = 1
df.loc[df["sma_20"] <= df["sma_50"], "signal"] = 0

# 4. Daily returns
df["daily_return"] = df["close"].pct_change()

# 5. Strategy returns (use yesterday's signal)
df["strategy_return"] = df["daily_return"] * df["signal"].shift(1)

# 6. Equity curves
initial_capital = 100_000

df["equity"] = initial_capital * (1 + df["strategy_return"]).cumprod()
df["buy_hold_equity"] = initial_capital * (1 + df["daily_return"]).cumprod()

# DEBUG CHECK (do NOT remove yet)
print("COLUMNS:", df.columns)

# 7. Results
final_capital = df["equity"].iloc[-1]
total_return = (final_capital / initial_capital - 1) * 100

print(f"Initial capital: ₹{initial_capital:,.0f}")
print(f"Final capital:   ₹{final_capital:,.0f}")
print(f"Total return:    {total_return:.2f}%")

# 8. Plot
plt.figure(figsize=(12, 6))
plt.plot(df.index, df["equity"], label="SMA Strategy")
plt.plot(df.index, df["buy_hold_equity"], label="Buy & Hold", linestyle="--")

plt.title("Equity Curve: SMA Strategy vs Buy & Hold")
plt.xlabel("Date")
plt.ylabel("Portfolio Value (₹)")
plt.legend()
plt.grid(True)

plt.show()
