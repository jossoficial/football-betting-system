import numpy as np
import pandas as pd
from itertools import product

def poisson_prob(lmbda, k):
    return (np.exp(-lmbda) * lmbda**k) / np.math.factorial(k)

def match_prediction(home_xg, away_xg):
    max_goals = 5

    matrix = np.zeros((max_goals, max_goals))

    for i, j in product(range(max_goals), range(max_goals)):
        matrix[i][j] = poisson_prob(home_xg, i) * poisson_prob(away_xg, j)

    home_win = np.sum(np.tril(matrix, -1))
    draw = np.sum(np.diag(matrix))
    away_win = np.sum(np.triu(matrix, 1))

    over_25 = np.sum(matrix[i][j] for i in range(max_goals) for j in range(max_goals) if i+j > 2)

    return {
        "home_win": round(home_win, 2),
        "draw": round(draw, 2),
        "away_win": round(away_win, 2),
        "over_2_5": round(over_25, 2)
    }
