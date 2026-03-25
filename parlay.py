def build_parlays(all_values):
    parlays = []

    # ordenar partidos por mejor pick
    sorted_matches = sorted(
        all_values,
        key=lambda x: x["values"][0]["score"] if x["values"] else 0,
        reverse=True
    )

    # tomar solo los mejores 3 partidos
    top_matches = sorted_matches[:3]

    parlay = []

    for match in top_matches:
        best_pick = match["values"][0]
        parlay.append({
            "match": match["match"],
            "pick": best_pick
        })

    return parlay
