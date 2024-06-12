from core.analysis import spectral_centroid
from core.analysis import comparisons
import numpy as np


def calculate_spectral_roll_off(audio_signal: np.ndarray, sample_rate: float,
                                n_fft: int = 512, roll_percent: float = 0.5) -> float:
    spectral_centroids = spectral_centroid.calculate_spectral_centroid(audio_signal, sample_rate, n_fft)

    frequencies = np.linspace(0, sample_rate, len(spectral_centroids))
    cumulative_sum = np.cumsum(spectral_centroids)
    # The last element is the total cumulative sum of the spectral centroids
    total_sum = cumulative_sum[-1]

    return float(np.interp(roll_percent, cumulative_sum / total_sum, frequencies))


def compare_two_spectral_roll_off(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                                  sample_rate1: float, sample_rate2: float,
                                  n_fft: int = 512, roll_percent: float = 0.5) -> float:
    roll_off1 = calculate_spectral_roll_off(audio_signal1, sample_rate1, n_fft, roll_percent)
    roll_off2 = calculate_spectral_roll_off(audio_signal2, sample_rate2, n_fft, roll_percent)

    similarity_percentage = comparisons.round_to_one(
        comparisons.normalized_relative_difference_individual(roll_off1, roll_off2))

    return max(0.0, similarity_percentage)


def compare_multiple_spectral_roll_off(audio_signals: list, sample_rates: list,
                                       n_fft: int = 512, roll_percent: float = 0.5) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_spectral_roll_off(audio_signals[i], audio_signals[j],
                                                       sample_rates[i], sample_rates[j], n_fft, roll_percent)
            similarity_values.append(similarity)

    mean_similarity = comparisons.round_to_one(np.mean(similarity_values))

    return mean_similarity
