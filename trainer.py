import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier

def train_model():
    df = pd.read_csv("storage/matches.csv")

    if len(df) < 10:
        return None

    X = df[["home_xg","away_xg"]]
    y = (df["home_xg"] > df["away_xg"]).astype(int)

    model = GradientBoostingClassifier()
    model.fit(X, y)

    return model
