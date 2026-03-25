def select_best_markets(pred, roi_data):
    selected = []

    for market, prob in pred.items():
        roi = roi_data.get(market, 0)

        # 🔥 DOBLE FILTRO (CLAVE)
        if prob > 0.55 and roi > 0:
            selected.append({
                "market": market,
                "prob": prob,
                "roi": roi,
                "score": prob * (1 + roi)
            })

    selected = sorted(selected, key=lambda x: x["score"], reverse=True)

    return selected[:2]  # máximo 2 picks por partido
