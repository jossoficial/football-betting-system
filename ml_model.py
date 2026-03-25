import pandas as pd
from sklearn.ensemble import RandomForestClassifier

def train_model():
    df = pd.read_csv("data/training.csv")

    X = df.drop("result", axis=1)
    y = df["result"]

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    return model

def predict_ml(model, features):
    prob = model.predict_proba([features])[0][1]
    return prob
