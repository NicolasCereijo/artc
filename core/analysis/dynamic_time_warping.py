from core.analysis import comparisons
from .mfcc import calculate_mfcc
import numpy as np
import librosa


def compare_two_dtw(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                    sample_rate1: float, sample_rate2: float, n_fft: int = 1024) -> float:
    mfcc1 = calculate_mfcc(audio_signal1, sample_rate1, n_fft)
    mfcc2 = calculate_mfcc(audio_signal2, sample_rate2, n_fft)

    _, optimal_alignment_path = librosa.sequence.dtw(X=mfcc1, Y=mfcc2, metric='cosine')

    aligned_mfcc1 = mfcc1[optimal_alignment_path[:, 0]]
    aligned_mfcc2 = mfcc2[optimal_alignment_path[:, 1]]

    similarity_percentage = comparisons.round_to_one(
        comparisons.pearson_correlation(aligned_mfcc1, aligned_mfcc2))

    return max(0.0, similarity_percentage)


def compare_multiple_dtw(audio_signals: list, sample_rates: list, n_fft: int = 1024) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_dtw(audio_signals[i], audio_signals[j],
                                         sample_rates[i], sample_rates[j], n_fft)
            similarity_values.append(similarity)

    mean_similarity = comparisons.round_to_one(np.mean(similarity_values))

    return mean_similarity
