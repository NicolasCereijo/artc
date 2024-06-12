from core.analysis import comparisons
import numpy as np
import librosa


def calculate_temporal_flux(audio_signal: np.ndarray, sample_rate: float, hop_length: int = 8192) -> np.ndarray:
    return librosa.onset.onset_strength(y=audio_signal, sr=sample_rate, hop_length=hop_length)


def compare_two_temporal_flux(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                              sample_rate1: float, sample_rate2: float, hop_length: int = 8192) -> float:
    flux1 = calculate_temporal_flux(audio_signal1, sample_rate1, hop_length)
    flux2 = calculate_temporal_flux(audio_signal2, sample_rate2, hop_length)

    similarity_percentage = comparisons.round_to_one(
        comparisons.normalized_relative_difference_array(flux1, flux2))

    return max(0.0, similarity_percentage)


def compare_multiple_temporal_flux(audio_signals: list, sample_rates: list, hop_length: int = 8192) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_temporal_flux(audio_signals[i], audio_signals[j],
                                                   sample_rates[i], sample_rates[j], hop_length)
            similarity_values.append(similarity)

    mean_similarity = comparisons.round_to_one(np.mean(similarity_values))

    return mean_similarity
