import requests
import json
import re

def get_understat_data():
    url = "https://understat.com/league/EPL"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        html = response.text

        json_data = re.search(r"teamsData\s*=\s*JSON\.parse\('(.*)'\)", html)

        # 🔥 SI FALLA → fallback
        if not json_data:
            return fallback_data()

        data = json.loads(json_data.group(1).encode('utf-8').decode('unicode_escape'))

        teams = []

        for team_id, team in data.items():
            history = team["history"][-5:]

            xg = sum(float(m["xG"]) for m in history) / len(history)
            xga = sum(float(m["xGA"]) for m in history) / len(history)

            teams.append({
                "team": team["title"],
                "xg": round(xg, 2),
                "xga": round(xga, 2)
            })

        return teams

    except Exception as e:
        print("⚠️ Error Understat:", e)
        return fallback_data()


# 🔥 DATOS DE RESPALDO (MUY IMPORTANTE)
def fallback_data():
    return [
        {"team": "Arsenal", "xg": 2.1, "xga": 1.0},
        {"team": "Manchester City", "xg": 2.5, "xga": 0.9},
        {"team": "Liverpool", "xg": 2.3, "xga": 1.1},
        {"team": "Chelsea", "xg": 1.8, "xga": 1.2},
        {"team": "Tottenham", "xg": 2.0, "xga": 1.3},
        {"team": "Manchester United", "xg": 1.9, "xga": 1.4},
    ]
