import csv
import os

FILE = "storage/matches.csv"

def save_match(home, away, home_xg, away_xg):
    os.makedirs("storage", exist_ok=True)

    file_exists = os.path.isfile(FILE)

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["home","away","home_xg","away_xg"])

        writer.writerow([home, away, home_xg, away_xg])
