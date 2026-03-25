import requests
import os

def get_odds():
    API_KEY = os.getenv("ODDS_API_KEY")

    url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey={API_KEY}&regions=eu&markets=h2h,totals"

    response = requests.get(url)
    data = response.json()

    matches = []

    for game in data:
        home = game["home_team"]
        away = game["away_team"]

        odds = {}
        over_odds = None
        under_odds = None

        for bookmaker in game["bookmakers"]:
            for market in bookmaker["markets"]:
                
                if market["key"] == "h2h":
                    for o in market["outcomes"]:
                        odds[o["name"]] = o["price"]

                if market["key"] == "totals":
                    for o in market["outcomes"]:
                        if o["name"] == "Over":
                            over_odds = o["price"]
                        if o["name"] == "Under":
                            under_odds = o["price"]

        matches.append({
            "home": home,
            "away": away,
            "odds": odds,
            "over": over_odds,
            "under": under_odds
        })

    return matches
