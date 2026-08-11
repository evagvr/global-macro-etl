import pandas as pd

def transform(df_fred: pd.DataFrame, df_stocks: pd.DataFrame, df_forex: pd.DataFrame):
    df_merged = df_fred.join(df_stocks, how="outer")
    df_merged["value"] = df_merged["value"].ffill()
    df_merged = df_merged.dropna(subset=["close"])
    df_merged = df_merged.join(df_forex, how="left")
    elements_list = ["close", "open", "high", "low"]
    for element in elements_list:
        df_merged[element] = df_merged[element] * df_merged["USDEUR"]
    return df_merged