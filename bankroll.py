def kelly(prob, odds):
    b = odds - 1
    q = 1 - prob

    kelly_fraction = (b * prob - q) / b

    return max(0, min(kelly_fraction, 0.05))
