def find_value(pred, odds):
    value_bets = []

    for key in pred:
        if key not in odds or odds[key] is None:
            continue

        prob = pred[key]
        odd = odds[key]
        implied = 1 / odd
        edge = prob - implied

        if prob < 0.60:
            continue

        if edge < 0.07:
            continue

        if key not in ["over_2_5", "under_3_5", "home_win"]:
            continue

        value_bets.append({
            "market": key,
            "prob": round(prob, 2),
            "odds": odd,
            "edge": round(edge, 2),
            "score": round(prob * edge, 3)
        })

    value_bets = sorted(value_bets, key=lambda x: x["score"], reverse=True)

    return value_bets
