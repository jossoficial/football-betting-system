from understat_scraper import get_understat_data
from odds_api import get_odds
from model import predict_match
from data_collector import save_match
from trainer import train_model
from evaluator import evaluate
from strategy import select_best_markets

def run_pipeline():
    teams = get_understat_data()
    odds_matches = get_odds()

    roi_data = evaluate()
    model = train_model()

    print("\n🏦 SISTEMA INSTITUCIONAL 🏦\n")

    for i in range(min(len(teams)-1, len(odds_matches))):
        home = teams[i]
        away = teams[i+1]

        save_match(home["team"], away["team"], home["xg"], away["xg"])

        pred = predict_match(home["xg"], away["xg"])

        best = select_best_markets(pred, roi_data)

        if best:
            print(f"{home['team']} vs {away['team']}")
            for b in best:
                print(f"- {b['market']} | prob: {round(b['prob'],2)} | ROI hist: {b['roi']}")
            print()
