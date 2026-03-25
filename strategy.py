def select_best_markets(pred, roi_data):
    selected = []

    for market, prob in pred.items():
        roi = roi_data.get(market, 0)

        # solo mercados rentables históricamente
        if roi > 0.05 and prob > 0.6:
            selected.append({
                "market": market,
                "prob": prob,
                "roi": roi
            })

    return selected
