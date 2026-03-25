def build_parlays(all_values):
    parlays = []

    sorted_matches = sorted(
        all_values,
        key=lambda x: x["values"][0]["score"] if x["values"] else 0,
        reverse=True
    )

    top_matches = sorted_matches[:3]

    for match in top_matches:
        best_pick = match["values"][0]
        parlays.append({
            "match": match["match"],
            "pick": best_pick
        })

    return parlays
