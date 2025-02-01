import numpy as np
from librosa import times_like
from librosa.onset import onset_strength


def calculate_temporal_centroid(audio_signal: np.ndarray, sample_rate: float, /) -> np.ndarray:
    envelope = np.abs(onset_strength(y=audio_signal, sr=sample_rate))
    times = times_like(envelope, sr=sample_rate)

    temporal_centroid = np.sum(envelope * times) / np.sum(envelope)
    return np.array([temporal_centroid])


def compare_two_temporal_centroid(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                                  sample_rate1: float, sample_rate2: float, /) -> float:
    centroid_1 = calculate_temporal_centroid(audio_signal1, sample_rate1)
    centroid_2 = calculate_temporal_centroid(audio_signal2, sample_rate2)

    distance = np.linalg.norm(np.abs(centroid_1) -
                              np.abs(centroid_2))
    max_distance = (np.linalg.norm(np.abs(centroid_1)) +
                    np.linalg.norm(np.abs(centroid_2)))

    similarity = (1 - distance / max_distance) if max_distance > 0 else 1.0
    return float(similarity)


def compare_multiple_temporal_centroid(audio_signals: list, sample_rates: list, /) -> float:
    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_temporal_centroid(
                audio_signals[i], audio_signals[j],
                sample_rates[i], sample_rates[j]
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
