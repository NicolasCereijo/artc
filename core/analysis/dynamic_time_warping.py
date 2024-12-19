import numpy as np
from librosa.sequence import dtw

from .mfcc import calculate_mfcc


def compare_two_dtw(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                    sample_rate1: float, sample_rate2: float,
                    /, *, n_fft: int = 1024) -> float:
    mfcc1 = calculate_mfcc(audio_signal1, sample_rate1, n_fft=n_fft)
    mfcc2 = calculate_mfcc(audio_signal2, sample_rate2, n_fft=n_fft)

    distance, _ = dtw(X=mfcc1, Y=mfcc2)
    dtw_distance = distance[-1, -1]
    max_distance = max(mfcc1.shape[1], mfcc2.shape[1])

    similarity = (dtw_distance / max_distance) if max_distance > 0 else 1.0
    return max(0.0, 1 - similarity / 100)


def compare_multiple_dtw(audio_signals: list, sample_rates: list,
                         /, *, n_fft: int = 1024) -> float:
    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_dtw(
                audio_signals[i], audio_signals[j],
                sample_rates[i], sample_rates[j],
                n_fft=n_fft
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
