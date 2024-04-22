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


def calculate_zcr(*signals: tuple) -> np.ndarray[..., np.dtype]:
    zcr_values = [0.0] * len(signals[0])
    for i in range(0, len(signals[0])):
        zcr_values[i] += librosa.feature.zero_crossing_rate(y=signals[0][i])

    return np.array(zcr_values)


def compare_zcr(*audio_signals: np.ndarray[float, ...]) -> float:
    if len(audio_signals) < 2:
        raise ValueError("At least two signals must be passed as parameters")

    adjusted_signals = calculate_zcr(harmonize.adjust_length(*audio_signals))
    normalized_signals = [arr[0].tolist() for arr in harmonize.normalize_btw_0_1(adjusted_signals)[0]]
    correlation_coefficient = np.corrcoef(normalized_signals)

    result = np.mean(correlation_coefficient[0, 1:])
    if result > 0.999:
        result = 1

    return max(result, 0)
