import pandas as pd

def add_indicadors(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona indicadores ao DataFrame.
    """
    df["Return"] = df["ADj Close"].pct_change
    df["CumReturn"] = (1 + df["Return"]).cumprod() -1 
    df["MA20"] = df["ADj Close"].rolling(window=20).mean()
    df["MA50"] = df["ADj Close"].rolling(window=50).mean()
    return df


def summarize(df: pd.DataFrame) -> dict:
    df_valid = df.dropna (subset=["Return"])
    total_return = df_valid["CumReturn"].iloc[-1]
    avg_daily = df_valid["Return"].mean()
    vol_daily = df_valid["Return"].std()
    stats = {
        "total_return": total_return,
        "avg_daily_return": avg_daily,
        "daily_volatility": vol_daily,
    }
    return stats

import pandas as pd

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Return"] = df["Adj Close"].pct_change()
    df["CumReturn"] = (1 + df["Return"]).cumprod() - 1
    df["MA20"] = df["Adj Close"].rolling(window=20).mean()
    df["MA50"] = df["Adj Close"].rolling(window=50).mean()
    return df
