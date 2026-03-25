from understat_scraper import get_understat_data
from odds_api import get_odds
from model import predict_match
from value import find_value
from parlay import build_parlays
from bankroll import kelly
from tracker import calculate_roi

BANKROLL = 1000  # dinero inicial

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

    print("\n🏦 HEDGE FUND MODE 🏦\n")

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

    parlays = build_parlays(all_values)

    print("🎯 PICKS + GESTIÓN DE BANCA:\n")

    for p in parlays:
        pick = p["pick"]

        stake_pct = kelly(pick["prob"], pick["odds"])
        stake = round(BANKROLL * stake_pct, 2)

        print(p["match"])
        print(f"- {pick['market']}")
        print(f"  cuota: {pick['odds']}")
        print(f"  prob: {pick['prob']}")
        print(f"  stake recomendado: ${stake} ({round(stake_pct*100,2)}%)\n")

    roi = calculate_roi()
    print(f"\n📈 ROI HISTÓRICO: {roi}%\n")


if __name__ == "__main__":
    main()
