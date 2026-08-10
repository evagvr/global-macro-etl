import pandas as pd

def transform(data: dict):
    observations = data["observations"]
    df = pd.DataFrame(observations)
    df = df.drop(columns=["realtime_start", "realtime_end"])
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    df["value"] = df["value"].astype(float)
    return df