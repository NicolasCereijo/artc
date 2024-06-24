from core.analysis import comparisons
import numpy as np
import librosa


def calculate_loudness(audio_signal: np.ndarray, /) -> np.ndarray:
    magnitude_spectrogram = np.abs(librosa.stft(audio_signal))
    return librosa.amplitude_to_db(magnitude_spectrogram, ref=np.max)[0]


def compare_two_loudness(audio_signal1: np.ndarray, audio_signal2: np.ndarray, /) -> float:
    loudness1 = calculate_loudness(audio_signal1)
    loudness2 = calculate_loudness(audio_signal2)

    similarity_percentage = comparisons.round_to_one(
        comparisons.normalized_euclidean_distance(loudness1, loudness2))

    return max(0.0, similarity_percentage)


def compare_multiple_loudness(audio_signals: list, /) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_loudness(audio_signals[i], audio_signals[j])
            similarity_values.append(similarity)

    mean_similarity = comparisons.round_to_one(np.mean(similarity_values))

    return mean_similarity
