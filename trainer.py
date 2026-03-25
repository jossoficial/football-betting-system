import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from historical_data import load_historical_data, build_training_dataset

def train_model():

    # 🔥 cargar data masiva
    raw_df = load_historical_data()
    df = build_training_dataset(raw_df)

    if len(df) < 50:
        return None

    X = df.drop("result", axis=1)
    y = df["result"]

    model = GradientBoostingClassifier()
    model.fit(X, y)

    return model
