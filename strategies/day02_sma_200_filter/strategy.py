from utils.data_loader import load_price_data
from utils.indicators import sma


df = load_price_data("ETERNAL.NS", start="2021-01-01")

df["sma_20"] = sma(df["close"], 20)
df["sma_50"] = sma(df["close"], 50)
df["sma_200"] = sma(df["close"], 200)

df["signal"] = 0

trend_ok = df["close"] > df["sma_200"]
entry = df["sma_20"] > df["sma_50"]

df.loc[trend_ok & entry, "signal"] = 1
df.loc[~trend_ok | (df["sma_20"] <= df["sma_50"]), "signal"] = 0

print(df[["close", "sma_20", "sma_50", "sma_200", "signal"]].tail(10))
