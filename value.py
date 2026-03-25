def calculate_ev(prob, odds):
    return (prob * odds) - 1


def find_value(pred, odds):
    value_bets = []

    for market in pred:

        if market not in odds or odds[market] is None:
            continue

        prob = pred[market]
        odd = odds[market]

        ev = calculate_ev(prob, odd)

        # 🔥 FILTROS PROFESIONALES
        if prob < 0.55:
            continue

        if ev < 0.05:  # mínimo 5% EV
            continue

        value_bets.append({
            "market": market,
            "prob": round(prob, 3),
            "odds": odd,
            "ev": round(ev, 3),
            "score": round(ev * prob, 4)
        })

    value_bets = sorted(value_bets, key=lambda x: x["score"], reverse=True)

    return value_bets
