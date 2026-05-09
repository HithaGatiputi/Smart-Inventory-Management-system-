
import pandas as pd
import numpy as np

def build_features(df):

    df["date"] = pd.to_datetime(df["date"])

    df["month"] = df["date"].dt.month

    df["month_sin"] = np.sin(
        2 * np.pi * df["month"] / 12
    )

    df["month_cos"] = np.cos(
        2 * np.pi * df["month"] / 12
    )

    return df
