def kelly(prob, odds):
    b = odds - 1
    q = 1 - prob

    k = (b * prob - q) / b

    # 🔥 CONTROL PROFESIONAL
    return max(0, min(k, 0.03))  # máximo 3%
