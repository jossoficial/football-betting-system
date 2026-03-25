def format_pick(p):
    return (
        f"{p['match']}\n"
        f"→ {p['market']}\n"
        f"Cuota: {p['odds']}\n"
        f"Prob: {p['prob']}\n"
        f"EV: {p['ev']}\n"
        f"Stake: ${p['stake']}\n"
    )


def send_report(picks):
    print("\n🚀 PICKS FINALES 🚀\n")

    for p in picks:
        print(format_pick(p))
