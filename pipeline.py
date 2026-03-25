from understat_scraper import get_understat_data
from odds_api import get_odds
from model import predict_match, combine_models
from data_collector import save_match
from trainer import train_model
from evaluator import evaluate
from features import build_features
from ml_model import predict_ml
from value import find_value
from bankroll import kelly
from logger import log_bet


def run_pipeline():
    teams = get_understat_data()
    odds_matches = get_odds()

    roi_data = evaluate()
    model = train_model()

    picks = []

    print("\n🏆 SISTEMA ELITE FINAL 🏆\n")

    for o in odds_matches:
        home = None
        away = None

        for t in teams:
            if t["team"].lower() in o["home"].lower():
                home = t
            if t["team"].lower() in o["away"].lower():
                away = t

        if not home or not away:
            continue

        save_match(home["team"], away["team"], home["xg"], away["xg"])

        features = build_features(home, away)
        ml_prob = predict_ml(model, features) if model else 0.5

        poisson = predict_match(home["xg"], away["xg"])
        combined = combine_models(poisson["home_win"], ml_prob)

        pred = {
            "home_win": combined,
            "over_2_5": poisson["over_2_5"],
            "under_3_5": poisson["under_3_5"]
        }

        odds_map = {
            "home_win": o["odds"].get(o["home"]),
            "over_2_5": o["over"],
            "under_3_5": o["under"]
        }

        values = find_value(pred, odds_map)

        if not values:
            continue

        best = values[0]

        # 🔥 FILTRO FINAL PROFESIONAL
        if best["prob"] < 0.6 or best["ev"] < 0.05:
            continue

        stake_pct = kelly(best["prob"], best["odds"])
        stake = round(1000 * stake_pct, 2)

        pick = {
            "match": f"{home['team']} vs {away['team']}",
            "market": best["market"],
            "prob": best["prob"],
            "odds": best["odds"],
            "ev": best["ev"],
            "stake": stake
        }

        picks.append(pick)

        # 💾 guardar apuesta
        log_bet(pick["match"], pick["market"], pick["odds"])

    # ordenar picks
    picks = sorted(picks, key=lambda x: x["ev"], reverse=True)[:3]

    return picks
