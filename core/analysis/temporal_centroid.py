from core.analysis import comparisons
import numpy as np
import librosa


def calculate_temporal_centroid(audio_signal: np.ndarray, sample_rate: float, /) -> float:
    envelope = np.abs(librosa.onset.onset_strength(y=audio_signal, sr=sample_rate))
    times = librosa.times_like(envelope, sr=sample_rate)
    return np.sum(envelope * times) / np.sum(envelope)


def compare_two_temporal_centroid(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                                  sample_rate1: float, sample_rate2: float, /) -> float:
    centroid1 = calculate_temporal_centroid(audio_signal1, sample_rate1)
    centroid2 = calculate_temporal_centroid(audio_signal2, sample_rate2)

    similarity_percentage = comparisons.round_to_one(
        comparisons.normalized_relative_difference_individual(centroid1, centroid2))

    return max(0.0, similarity_percentage)


def compare_multiple_temporal_centroid(audio_signals: list, sample_rates: list, /) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_temporal_centroid(audio_signals[i], audio_signals[j],
                                                       sample_rates[i], sample_rates[j])
            similarity_values.append(similarity)

    mean_similarity = comparisons.round_to_one(np.mean(similarity_values))

    return mean_similarity
