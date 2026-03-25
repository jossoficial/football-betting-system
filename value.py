def find_value_bets(predictions):
    # cuotas simuladas (luego conectamos API real)
    odds = {
        "home_win": 1.80,
        "draw": 3.50,
        "away_win": 4.00,
        "over_2_5": 1.90
    }

    value_bets = []

    for key in predictions:
        prob = predictions[key]
        implied = 1 / odds[key]

        if prob > implied:
            value_bets.append({
                "market": key,
                "prob": prob,
                "odds": odds[key]
            })

    return value_bets
