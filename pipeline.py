from understat_scraper import get_understat_data
from odds_api import get_odds
from model import predict_match, combine_models
from data_collector import save_match
from trainer import train_model
from evaluator import evaluate
from strategy import select_best_markets
from ml_model import predict_ml
from features import build_features
from value import find_value


def run_pipeline():
    teams = get_understat_data()
    odds_matches = get_odds()

    roi_data = evaluate()
    model = train_model()

    print("\n🏦 SISTEMA ELITE ACTIVO 🏦\n")

    all_picks = []

    for o in odds_matches:
        home = None
        away = None

        # 🔍 MATCH EQUIPOS
        for t in teams:
            if t["team"].lower() in o["home"].lower():
                home = t
            if t["team"].lower() in o["away"].lower():
                away = t

        if not home or not away:
            continue

        # 💾 GUARDAR DATA
        save_match(home["team"], away["team"], home["xg"], away["xg"])

        # 🧠 FEATURES ML
        features = build_features(home, away)

        # 🤖 PREDICCIÓN ML
        ml_prob = predict_ml(model, features) if model else 0.5

        # 📊 POISSON
        poisson = predict_match(home["xg"], away["xg"])

        # 🔀 COMBINACIÓN MODELOS
        combined_home = combine_models(poisson["home_win"], ml_prob)

        pred = {
            "home_win": combined_home,
            "over_2_5": poisson["over_2_5"],
            "under_3_5": poisson["under_3_5"]
        }

        # 📊 MAPEAR ODDS
        odds_map = {
            "home_win": o["odds"].get(o["home"]),
            "over_2_5": o["over"],
            "under_3_5": o["under"]
        }

        # 💰 VALUE BETS (EV REAL)
        values = find_value(pred, odds_map)

        if not values:
            continue

        # 🎯 FILTRO FINAL (ULTRA IMPORTANTE)
        values = [v for v in values if v["prob"] > 0.6 and v["ev"] > 0.05]

        if not values:
            continue

        # 🧠 ESTRATEGIA + ROI
        best_markets = select_best_markets(pred, roi_data)

        if not best_markets:
            continue

        best = values[0]

        pick = {
            "match": f"{home['team']} vs {away['team']}",
            "market": best["market"],
            "prob": best["prob"],
            "odds": best["odds"],
            "ev": best["ev"]
        }

        all_picks.append(pick)

    # 🏆 ORDENAR PICKS (MEJORES PRIMERO)
    all_picks = sorted(all_picks, key=lambda x: x["ev"], reverse=True)

    print("🎯 PICKS ELITE:\n")

    for p in all_picks[:3]:
        print(p["match"])
        print(f"- {p['market']}")
        print(f"  prob: {p['prob']}")
        print(f"  cuota: {p['odds']}")
        print(f"  EV: {p['ev']}\n")
