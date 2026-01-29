import pandas as pd

from utils.data_loader import load_price_data
from utils.indicators import sma


# 1. Load data
df = load_price_data("SBIN.NS", start="2022-01-01")

# 2. Indicators
df["sma_20"] = sma(df["close"], 20)
df["sma_50"] = sma(df["close"], 50)

# 3. Signals
df["signal"] = 0
df.loc[df["sma_20"] > df["sma_50"], "signal"] = 1
df.loc[df["sma_20"] < df["sma_50"], "signal"] = 0  # exit to cash

# 4. Daily returns
df["daily_return"] = df["close"].pct_change()

# 5. Strategy returns
df["strategy_return"] = df["daily_return"] * df["signal"].shift(1)

# 6. Equity curve
initial_capital = 100_000
df["equity"] = initial_capital * (1 + df["strategy_return"]).cumprod()

# 7. Results
final_capital = df["equity"].iloc[-1]
total_return = (final_capital / initial_capital - 1) * 100

print(f"Initial capital: ₹{initial_capital:,.0f}")
print(f"Final capital:   ₹{final_capital:,.0f}")
print(f"Total return:    {total_return:.2f}%")
