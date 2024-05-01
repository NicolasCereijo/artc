import core.datastructures as dt_structs
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def round_to_one(number: float) -> float:
    if number > 0.999:
        number = 1
    return number


def pearson_correlation(array1: np.ndarray, array2: np.ndarray) -> float:
    vector1, vector2 = dt_structs.adjust_dimensions(array1, array2)

    correlation = np.corrcoef(vector1.flatten(), vector2.flatten())[0, 1]
    similarity_percentage = (correlation + 1) / 2

    return similarity_percentage


def cosine_similarity_coefficient(array1: np.ndarray, array2: np.ndarray) -> float:
    vector1, vector2 = dt_structs.adjust_dimensions(array1, array2)

    similarity_percentage = cosine_similarity(vector1, vector2)[0][0]
    return similarity_percentage


def normalized_relative_difference_individual(value1: float, value2: float) -> float:
    similarity_percentage = 1 - (abs(value1 - value2) / max(value1, value2))
    return similarity_percentage


def normalized_relative_difference_array(array1: np.ndarray, array2: np.ndarray) -> float:
    similarity_percentage = 1 - (abs(array1 - array2) / max(array1.max(), array2.max()))
    similarity_percentage = np.mean(similarity_percentage)

    return similarity_percentage
