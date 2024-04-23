from core.artc_collections import harmonize
import numpy as np
import librosa


def check_zcr(signal: np.ndarray[float, ...]) -> tuple[bool, int]:
    if len(signal) == 0:
        return False, 0

    zc = librosa.zero_crossings(y=signal)
    check_any_zc = any(zc)
    count_zc = np.count_nonzero(zc)

    return check_any_zc, count_zc


def calculate_zcr(audio_signal: np.ndarray) -> np.ndarray[..., np.dtype]:
    return librosa.feature.zero_crossing_rate(y=audio_signal)


def compare_two_zcr(signal1: np.ndarray, signal2: np.ndarray) -> float:
    zcr1, zcr2 = harmonize.adjust_length(signal1, signal2)
    zcr1 = calculate_zcr(zcr1)
    zcr2 = calculate_zcr(zcr2)

    normalized_signals = [arr[0].tolist() for arr in harmonize.normalize_btw_0_1(zcr1, zcr2)]
    correlation_coefficient = np.corrcoef(normalized_signals)

    result = np.mean(correlation_coefficient[0, 1:])
    if result > 0.999:
        result = 1

    return max(result, 0)


def compare_multiple_zcr(audio_signals: list) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_zcr(audio_signals[i], audio_signals[j])
            similarity_values.append(similarity)

    mean_similarity = np.mean(similarity_values)

    if mean_similarity > 0.999:
        mean_similarity = 1

    return mean_similarity
