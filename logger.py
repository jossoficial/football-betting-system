import csv
import os

FILE = "storage/bets.csv"

def log_bet(match, market, odds):
    os.makedirs("storage", exist_ok=True)

    file_exists = os.path.isfile(FILE)

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["match","market","odds","result"])

        writer.writerow([match, market, odds, "pending"])
