import yfinance as yf
import pandas as pd


def load_price_data(
    symbol: str,
    start: str = "2018-01-01",
    end: str | None = None,
    interval: str = "1d"
) -> pd.DataFrame:

    df = yf.download(
        symbol,
        start=start,
        end=end,
        interval=interval,
        progress=False
    )

    if df.empty:
        raise ValueError(f"No data returned for symbol: {symbol}")

    # Clean column names (handle MultiIndex)
    if isinstance(df.columns[0], tuple):
        df.columns = [c[0].lower() for c in df.columns]
    else:
        df.columns = [c.lower() for c in df.columns]

    df.dropna(inplace=True)

    return df
