import pandas as pd

from utils.data_loader import load_price_data
from utils.indicators import sma

# Load historical price data
df = load_price_data(
    symbol="SBIN.NS",
    start="2022-01-01"
)

# Calculate moving averages
df["sma_20"] = sma(df["close"], window=20)
df["sma_50"] = sma(df["close"], window=50)


# Generate signals
df["signal"] = 0  # 0 = no position

df.loc[df["sma_20"] > df["sma_50"], "signal"] = 1
df.loc[df["sma_20"] < df["sma_50"], "signal"] = -1

print(df[["close", "sma_20", "sma_50", "signal"]].tail(10))

