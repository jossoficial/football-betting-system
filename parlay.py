def build_parlays(all_values):
    parlays = []

    for match in all_values:
        picks = match["values"]

        if len(picks) >= 2:
            parlays.append({
                "match": match["match"],
                "picks": picks[:3]
            })

    return parlays
