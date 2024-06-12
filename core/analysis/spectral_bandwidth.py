from core.analysis import comparisons
import numpy as np
import librosa


def calculate_spectral_bandwidth(audio_signal: np.ndarray, sample_rate: float, n_fft: int = 4096) -> np.ndarray:
    return librosa.feature.spectral_bandwidth(y=audio_signal, sr=sample_rate, n_fft=n_fft)[0]


def compare_two_spect_bandwidth(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                                sample_rate1: float, sample_rate2: float, n_fft: int = 4096) -> float:
    bandwidth1 = calculate_spectral_bandwidth(audio_signal1, sample_rate1, n_fft)
    bandwidth2 = calculate_spectral_bandwidth(audio_signal2, sample_rate2, n_fft)

    similarity_percentage = comparisons.round_to_one(
        comparisons.normalized_euclidean_distance(bandwidth1, bandwidth2))

    return max(0.0, similarity_percentage)


def compare_multiple_spect_bandwidth(audio_signals: list, sample_rates: list, n_fft: int = 4096) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_spect_bandwidth(audio_signals[i], audio_signals[j],
                                                     sample_rates[i], sample_rates[j], n_fft)
            similarity_values.append(similarity)

    mean_similarity = comparisons.round_to_one(np.mean(similarity_values))

    return mean_similarity
