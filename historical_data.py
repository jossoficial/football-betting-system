import pandas as pd

def load_historical_data():
    # dataset público (puedes ampliar luego)
    url = "https://www.football-data.co.uk/mmz4281/2324/E0.csv"

    df = pd.read_csv(url)

    # limpiar columnas clave
    df = df[[
        "HomeTeam",
        "AwayTeam",
        "FTHG",
        "FTAG",
        "B365H",
        "B365A"
    ]]

    df = df.dropna()

    return df


def build_training_dataset(df):
    data = []

    for _, row in df.iterrows():
        home_goals = row["FTHG"]
        away_goals = row["FTAG"]

        data.append({
            "home_xg": home_goals,
            "away_xg": away_goals,
            "home_xga": away_goals,
            "away_xga": home_goals,
            "home_form": 0,
            "away_form": 0,
            "result": 1 if home_goals > away_goals else 0
        })

    return pd.DataFrame(data)
