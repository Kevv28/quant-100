import pandas as pd


def sma(series: pd.Series, window: int) -> pd.Series:
    """
    Simple Moving Average (SMA)

    Parameters:
    - series: price series (usually close)
    - window: lookback period

    Returns:
    - pandas Series of SMA values
    """

    if window <= 0:
        raise ValueError("window must be > 0")

    return series.rolling(window=window).mean()
