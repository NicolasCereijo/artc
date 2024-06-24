from core.analysis import comparisons
import numpy as np
import librosa


def calculate_spectral_flatness(audio_signal: np.ndarray, /, *, n_fft: int = 8192) -> np.ndarray:
    return librosa.feature.spectral_flatness(y=audio_signal, n_fft=n_fft)[0]


def compare_two_spect_flatness(audio_signal1: np.ndarray, audio_signal2: np.ndarray, /, *, n_fft: int = 8192) -> float:
    flatness1 = calculate_spectral_flatness(audio_signal1, n_fft=n_fft)
    flatness2 = calculate_spectral_flatness(audio_signal2, n_fft=n_fft)

    similarity_percentage = comparisons.round_to_one(
        comparisons.normalized_relative_difference_array(flatness1, flatness2))

    return max(0.0, similarity_percentage)


def compare_multiple_spect_flatness(audio_signals: list, /, *, n_fft: int = 8192) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_spect_flatness(audio_signals[i], audio_signals[j], n_fft=n_fft)
            similarity_values.append(similarity)

    mean_similarity = comparisons.round_to_one(np.mean(similarity_values))

    return mean_similarity
