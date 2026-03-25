import csv
import os

FILE = "data/history.csv"

def save_bet(match, market, odds, result):
    file_exists = os.path.isfile(FILE)

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(["match", "market", "odds", "result"])

        writer.writerow([match, market, odds, result])


def calculate_roi():
    if not os.path.exists(FILE):
        return 0

    total_bets = 0
    profit = 0

    with open(FILE, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            total_bets += 1

            if row["result"] == "win":
                profit += float(row["odds"]) - 1
            else:
                profit -= 1

    if total_bets == 0:
        return 0

    return round((profit / total_bets) * 100, 2)
