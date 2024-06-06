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
    vector1, vector2 = dt_structs.adjust_length(array1, array2)

    similarity_percentage = 1 - (abs(vector1 - vector2) / max(vector1.max(), vector2.max()))
    similarity_percentage = np.mean(similarity_percentage)

    return similarity_percentage


def normalized_euclidean_distance(array1: np.ndarray, array2: np.ndarray) -> float:
    vector1, vector2 = dt_structs.adjust_dimensions(array1, array2)

    euclidean_distance = np.linalg.norm(vector1 - vector2)
    max_distance = np.linalg.norm(np.ones_like(vector1) * (np.max(vector1) - np.min(vector1)) +
                                  np.ones_like(vector2) * (np.max(vector2) - np.min(vector2)))
    normalized_distance = euclidean_distance / max_distance

    # The normalized distance approaches 0 for very similar vectors and 1 for
    # completely different vectors, the percentage is returned in reverse
    similarity_percentage = 1 - normalized_distance

    return similarity_percentage
