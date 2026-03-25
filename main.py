from understat_scraper import get_understat_data
from odds_api import get_odds
from model import predict_match, combine_models
from value import find_value
from parlay import build_parlays
from bankroll import kelly
from ml_model import train_model, predict_ml
from features import build_features

BANKROLL = 1000

def match_teams(teams, odds_matches):
    paired = []

    for o in odds_matches:
        home = None
        away = None

        for t in teams:
            if t["team"] in o["home"]:
                home = t
            if t["team"] in o["away"]:
                away = t

        if home and away:
            paired.append((home, away, o))

    return paired


def main():
    teams = get_understat_data()
    odds_matches = get_odds()

    ml_model = train_model()

    games = match_teams(teams, odds_matches)

    all_values = []

    print("\n🤖 SISTEMA IA PROFESIONAL 🤖\n")

    for home, away, odds in games:

        features = build_features(home, away)
        ml_prob = predict_ml(ml_model, features)

        poisson = predict_match(home["xg"], away["xg"])
        combined = combine_models(poisson["home_win"], ml_prob)

        pred = {
            "home_win": combined,
            "over_2_5": poisson["over_2_5"],
            "under_3_5": poisson["under_3_5"]
        }

        odds_map = {
            "home_win": odds["odds"].get(home["team"]),
            "over_2_5": odds["over"],
            "under_3_5": odds["under"]
        }

        values = find_value(pred, odds_map)

        if values:
            all_values.append({
                "match": f"{home['team']} vs {away['team']}",
                "values": values
            })

    parlays = build_parlays(all_values)

    print("🎯 PICKS OPTIMIZADOS:\n")

    for p in parlays:
        pick = p["pick"]

        stake_pct = kelly(pick["prob"], pick["odds"])
        stake = round(BANKROLL * stake_pct, 2)

        print(p["match"])
        print(f"- {pick['market']}")
        print(f"  cuota: {pick['odds']}")
        print(f"  prob: {pick['prob']}")
        print(f"  stake: ${stake}\n")


from pipeline import run_pipeline

if __name__ == "__main__":
    run_pipeline()
