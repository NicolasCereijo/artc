from core.analysis import comparisons
import numpy as np
import librosa


def calculate_mfcc(audio_signal: np.ndarray, sample_rate: float, /, *, n_fft: int = 8192) -> np.ndarray:
    return librosa.feature.mfcc(y=audio_signal, sr=sample_rate, n_mfcc=13, n_fft=n_fft)[0]


def compare_two_mfcc(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                     sample_rate1: float, sample_rate2: float, /, *, n_fft: int = 8192) -> float:
    mfcc1 = calculate_mfcc(audio_signal1, sample_rate1, n_fft=n_fft)
    mfcc2 = calculate_mfcc(audio_signal2, sample_rate2, n_fft=n_fft)

    similarity_percentage = comparisons.round_to_one(
        comparisons.cosine_similarity_coefficient(mfcc1, mfcc2))

    return max(0.0, similarity_percentage)


def compare_multiple_mfcc(audio_signals: list, sample_rates: list, /, *, n_fft: int = 8192) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_mfcc(audio_signals[i], audio_signals[j],
                                          sample_rates[i], sample_rates[j], n_fft=n_fft)
            similarity_values.append(similarity)

    mean_similarity = comparisons.round_to_one(np.mean(similarity_values))

    return mean_similarity
