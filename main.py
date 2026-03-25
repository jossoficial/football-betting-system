from understat_scraper import get_understat_data
from model import match_prediction
from value import find_value_bets

def create_matches(teams):
    matches = []

    for i in range(0, len(teams)-1, 2):
        matches.append((teams[i], teams[i+1]))

    return matches


def main():
    teams = get_understat_data()
    matches = create_matches(teams)

    print("\n🔥 ANALISIS PROFESIONAL 🔥\n")

    for home, away in matches:
        pred = match_prediction(home["xg"], away["xg"])
        values = find_value_bets(pred)

        print(f"{home['team']} vs {away['team']}")
        print("Probabilidades:", pred)

        if values:
            print("💰 VALUE BETS:")
            for v in values:
                print(f"- {v['market']} (prob: {v['prob']} vs cuota: {v['odds']})")

        print("\n----------------------\n")


if __name__ == "__main__":
    main()
