import numpy as np
from librosa.feature import mfcc


def calculate_mfcc(audio_signal: np.ndarray, sample_rate: float,
                   /, *, n_fft: int = 2048) -> np.ndarray:
    return mfcc(y=audio_signal, sr=sample_rate, n_mfcc=13, n_fft=n_fft)


def compare_two_mfcc(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                     sample_rate1: float, sample_rate2: float,
                     /, *, n_fft: int = 2048) -> float:
    mfcc1 = np.fft.fft(calculate_mfcc(audio_signal1, sample_rate1, n_fft=n_fft))
    mfcc2 = np.fft.fft(calculate_mfcc(audio_signal2, sample_rate2, n_fft=n_fft))

    min_len = min(mfcc1.shape[1], mfcc2.shape[1])
    mfcc1_adjusted = mfcc1[:, :min_len]
    mfcc2_adjusted = mfcc2[:, :min_len]

    distance = np.linalg.norm(mfcc1_adjusted - mfcc2_adjusted)
    max_distance = (np.linalg.norm(mfcc1_adjusted) +
                    np.linalg.norm(mfcc2_adjusted))

    similarity = (1 - distance / max_distance) if max_distance > 0 else 1.0
    return float(similarity)


def compare_multiple_mfcc(audio_signals: list, sample_rates: list,
                          /, *, n_fft: int = 8192) -> float:
    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_mfcc(
                audio_signals[i], audio_signals[j],
                sample_rates[i], sample_rates[j],
                n_fft=n_fft
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
