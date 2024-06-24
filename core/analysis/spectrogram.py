from core.analysis import comparisons
import numpy as np
import librosa


def calculate_spectrogram(audio_signal: np.ndarray, /, *, n_fft: int = 4096) -> np.ndarray:
    return np.abs(librosa.stft(audio_signal, n_fft=n_fft))[0]


def compare_two_spectrograms(signal1: np.ndarray, signal2: np.ndarray, /, *, n_fft: int = 4096) -> float:
    spectrogram1 = calculate_spectrogram(signal1, n_fft=n_fft)
    spectrogram2 = calculate_spectrogram(signal2, n_fft=n_fft)

    similarity_percentage = comparisons.round_to_one(
        comparisons.cosine_similarity_coefficient(spectrogram1, spectrogram2))

    return max(0.0, similarity_percentage)


def compare_multiple_spectrograms(audio_signals: list, /, *, n_fft: int = 4096) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_spectrograms(audio_signals[i], audio_signals[j], n_fft=n_fft)
            similarity_values.append(similarity)

    mean_similarity = comparisons.round_to_one(np.mean(similarity_values))

    return mean_similarity
