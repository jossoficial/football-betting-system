from understat_scraper import get_understat_data
from odds_api import get_odds
from model import predict_match, combine_models
from data_collector import save_match
from trainer import train_model
from evaluator import evaluate
from strategy import select_best_markets
from ml_model import predict_ml
from features import build_features

def run_pipeline():
    teams = get_understat_data()
    odds_matches = get_odds()

    roi_data = evaluate()
    model = train_model()

    print("\n🏦 SISTEMA INSTITUCIONAL ACTIVO 🏦\n")

    for o in odds_matches:
        home = None
        away = None

        # match equipos correctamente
        for t in teams:
            if t["team"] in o["home"]:
                home = t
            if t["team"] in o["away"]:
                away = t

        if not home or not away:
            continue

        # guardar datos
        save_match(home["team"], away["team"], home["xg"], away["xg"])

        # features ML
        features = build_features(home, away)

        # predicción ML
        ml_prob = predict_ml(model, features) if model else 0.5

        # Poisson
        poisson = predict_match(home["xg"], away["xg"])

        # combinación
        combined = combine_models(poisson["home_win"], ml_prob)

        pred = {
            "home_win": combined,
            "over_2_5": poisson["over_2_5"],
            "under_3_5": poisson["under_3_5"]
        }

        best = select_best_markets(pred, roi_data)

        if best:
            print(f"{home['team']} vs {away['team']}")
            for b in best:
                print(f"- {b['market']} | prob: {round(b['prob'],2)} | ROI: {b['roi']}")
            print()
