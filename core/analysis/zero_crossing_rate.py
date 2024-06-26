import core.datastructures as dt_structs
from core.analysis import comparisons
import numpy as np
import librosa


def check_zcr(signal: np.ndarray, /) -> [bool, int]:
    if len(signal) == 0:
        return False, 0

    zc = librosa.zero_crossings(y=signal)
    check_any_zc = any(zc)
    count_zc = np.count_nonzero(zc)

    return check_any_zc, count_zc


def calculate_zcr(audio_signal: np.ndarray, /) -> np.ndarray:
    return librosa.feature.zero_crossing_rate(y=audio_signal)


def compare_two_zcr(signal1: np.ndarray, signal2: np.ndarray, /) -> float:
    zcr1 = calculate_zcr(signal1)
    zcr2 = calculate_zcr(signal2)

    zcr1_vector, zcr2_vector = [arr[0].tolist() for arr in dt_structs.normalize_btw_0_1(zcr1, zcr2)]
    zcr1_vector = np.array(zcr1_vector)
    zcr2_vector = np.array(zcr2_vector)

    similarity_percentage = comparisons.round_to_one(
        comparisons.normalized_relative_difference_array(zcr1_vector, zcr2_vector))

    return max(0.0, similarity_percentage)


def compare_multiple_zcr(audio_signals: list, /) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_zcr(audio_signals[i], audio_signals[j])
            similarity_values.append(similarity)

    mean_similarity = comparisons.round_to_one(np.mean(similarity_values))

    return mean_similarity
