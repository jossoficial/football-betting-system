from understat_scraper import get_understat_data
from odds_api import get_odds
from model import predict_match
from value import find_value
from parlay import build_parlays

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

    games = match_teams(teams, odds_matches)

    all_values = []

    print("\n🔥 SISTEMA ELITE 🔥\n")

    for home, away, odds in games:
        pred = predict_match(home["xg"], away["xg"])

        odds_map = {
            "home_win": odds["odds"].get(home["team"]),
            "away_win": odds["odds"].get(away["team"]),
            "over_2_5": odds["over"],
            "under_3_5": odds["under"]
        }

        values = find_value(pred, odds_map)

        if values:
            all_values.append({
                "match": f"{home['team']} vs {away['team']}",
                "values": values
            })

            print(f"{home['team']} vs {away['team']}")
            for v in values:
                print(f"- {v['market']} | prob: {v['prob']} | cuota: {v['odds']} | edge: {v['edge']}")
            print()

    parlays = build_parlays(all_values)

    print("\n🎯 PARLAY ULTRA ELITE:\n")

    for p in parlays:
        pick = p["pick"]
        print(p["match"])
        print(f"- {pick['market']} | cuota: {pick['odds']} | prob: {pick['prob']}")
        print()
