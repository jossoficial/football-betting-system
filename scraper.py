import requests

def get_matches():
    # API gratuita (ejemplo)
    url = "https://api.football-data.org/v4/matches"
    
    headers = {
        "X-Auth-Token": "TU_API_KEY"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    matches = []

    for match in data.get("matches", []):
        if match["status"] == "SCHEDULED":
            matches.append({
                "home": match["homeTeam"]["name"],
                "away": match["awayTeam"]["name"]
            })

    return matches
