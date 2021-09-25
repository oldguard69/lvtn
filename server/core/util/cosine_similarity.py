from numpy import dot
from math import sqrt

def cosine_sim(vector1, vector2) -> float:
    numerator = dot(vector1, vector2)
    denominator = sqrt(dot(vector1, vector1)) * sqrt(dot(vector2, vector2))
    return numerator / denominator