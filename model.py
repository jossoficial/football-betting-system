import numpy as np
from itertools import product

def poisson_prob(lmbda, k):
    return (np.exp(-lmbda) * lmbda**k) / np.math.factorial(k)

def predict_match(home_xg, away_xg):
    max_goals = 6
    matrix = np.zeros((max_goals, max_goals))

    for i, j in product(range(max_goals), range(max_goals)):
        matrix[i][j] = poisson_prob(home_xg, i) * poisson_prob(away_xg, j)

    home_win = np.sum(np.tril(matrix, -1))
    draw = np.sum(np.diag(matrix))
    away_win = np.sum(np.triu(matrix, 1))

    over_25 = sum(matrix[i][j] for i in range(max_goals) for j in range(max_goals) if i+j > 2)
    under_35 = sum(matrix[i][j] for i in range(max_goals) for j in range(max_goals) if i+j <= 3)

    return {
        "home_win": home_win,
        "draw": draw,
        "away_win": away_win,
        "over_2_5": over_25,
        "under_3_5": under_35
    }

def combine_models(poisson_prob, ml_prob):
    return (poisson_prob * 0.6) + (ml_prob * 0.4)
