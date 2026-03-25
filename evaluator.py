import pandas as pd

def evaluate():
    try:
        df = pd.read_csv("storage/bets.csv")
    except:
        return {}

    results = {}

    for market in df["market"].unique():
        subset = df[df["market"] == market]

        wins = subset[subset["result"] == "win"]
        losses = subset[subset["result"] == "loss"]

        profit = sum(wins["odds"] - 1) - len(losses)

        roi = profit / len(subset) if len(subset) > 0 else 0

        results[market] = round(roi, 2)

    return results
