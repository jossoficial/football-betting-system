def build_features(home, away):
    return [
        home["xg"],
        away["xg"],
        home["xga"],
        away["xga"],
        home["xg"] - away["xga"],  # ataque vs defensa
        away["xg"] - home["xga"],
    ]
