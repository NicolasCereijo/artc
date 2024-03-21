from core.artc_collections import harmonize
import numpy as np
import librosa


def check_zcr(signal: np.ndarray[float, ...]) -> tuple[bool, int]:
    """
        Check if the given signal has at least one zero crossing value.

        Arguments:
            signal (np.ndarray[float, ...]): Audio signal.

        Returns:
            check_zc (bool): True if the given signal has at least one zero crossing value,
            False if the given signal does not have any zero crossing value.
            count_zc (int): The number of zero crossing values.
    """
    if len(signal) == 0:
        return False, 0

    zc = librosa.zero_crossings(y=signal)
    check_zc = any(zc)
    count_zc = np.count_nonzero(zc)

    return check_zc, count_zc


def calculate_zcr(*signals: tuple) -> np.ndarray[..., np.dtype]:
    zcr_values = [0.0] * len(signals[0])
    for i in range(0, len(signals[0])):
        zcr_values[i] += librosa.feature.zero_crossing_rate(y=signals[0][i])

    return np.array(zcr_values)


def compare_zcr(*audio_signals: np.ndarray[float, ...]) -> float:
    """
        Compare the ZCR values of two or more signals stored in Numpy arrays.

        Args:
            *audio_signals (np.ndarray[float, ...]): Two or more audio signals.

        Returns:
            result (int): Average of the results of the comparisons. Value between 0 and 1, with 0 being
            completely different.
        Raises:
            ValueError: If there are not enough signals to compare.
    """
    if len(audio_signals) < 2:
        raise ValueError("At least two signals must be passed as parameters")

    adjusted_signals = calculate_zcr(harmonize.adjust_length(*audio_signals))
    normalized_signals = [arr[0].tolist() for arr in harmonize.normalize_btw_0_1(adjusted_signals)[0]]
    correlation_coefficient = np.corrcoef(normalized_signals)

    result = np.mean(correlation_coefficient[0, 1:])
    if result > 0.999:
        result = 1

    return max(result, 0)
