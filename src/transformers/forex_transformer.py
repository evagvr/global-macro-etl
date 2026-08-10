import pandas as pd

def transform(data: dict):
    quotes = data["quotes"]
    df = pd.DataFrame.from_dict(data=quotes, orient="index")
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    return df