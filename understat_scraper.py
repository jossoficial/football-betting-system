import requests
import json
import re

def get_understat_data():
    url = "https://understat.com/league/EPL"

    response = requests.get(url)
    html = response.text

    # extraer JSON embebido
    json_data = re.search(r"teamsData\s*=\s*JSON\.parse\('(.*)'\)", html)
    data = json.loads(json_data.group(1).encode('utf-8').decode('unicode_escape'))

    teams = []

    for team_id, team in data.items():
        history = team["history"][-5:]  # últimos 5 partidos

        xg = sum(float(m["xG"]) for m in history) / len(history)
        xga = sum(float(m["xGA"]) for m in history) / len(history)

        teams.append({
            "team": team["title"],
            "xg": round(xg, 2),
            "xga": round(xga, 2)
        })

    return teams
