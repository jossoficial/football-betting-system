def find_value(pred, odds):
    value_bets = []

    for key in pred:
        if key not in odds or odds[key] is None:
            continue

        prob = pred[key]
        odd = odds[key]

        implied = 1 / odd

        if prob > implied:
            edge = prob - implied

            if edge > 0.05:
                value_bets.append({
                    "market": key,
                    "prob": round(prob, 2),
                    "odds": odd,
                    "edge": round(edge, 2)
                })

    return value_bets
