import pandas as pd

def calculate(df):
    results = []

    for _, row in df.iterrows():
        home_strength = row['home_xg'] - row['away_xga'] + row['home_form']*0.1
        away_strength = row['away_xg'] - row['home_xga'] + row['away_form']*0.1

        total = abs(home_strength) + abs(away_strength) + 0.1
        home_prob = (home_strength + total) / (2 * total)

        total_xg = row['home_xg'] + row['away_xg']

        results.append({
            "match": f"{row['home_team']} vs {row['away_team']}",
            "home_win": round(home_prob,2),
            "over_1_5": round(min(0.95, total_xg/3),2),
            "under_4_5": 0.85 if total_xg < 4 else 0.65
        })

    return pd.DataFrame(results)

def parlays(df):
    output = []

    for _, row in df.iterrows():
        picks = []

        if row['over_1_5'] > 0.75:
            picks.append("Over 1.5")

        if row['under_4_5'] > 0.75:
            picks.append("Under 4.5")

        if row['home_win'] > 0.65:
            picks.append("Local gana")

        if len(picks) >= 2:
            output.append(f"\n{row['match']}\n" + "\n".join([f"- {p}" for p in picks[:3]]))

    return "\n".join(output)

def main():
    df = pd.read_csv("data/matches.csv")

    pred = calculate(df)
    parlays_result = parlays(pred)

    print("=== PREDICCIONES ===")
    print(pred.to_string())

    print("\n=== PARLAYS ===")
    print(parlays_result)

if __name__ == "__main__":
    main()
