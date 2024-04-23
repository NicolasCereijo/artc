from core.artc_collections import harmonize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import librosa


def calculate_spectrogram(audio_signal: np.ndarray, n_fft: int = 2048) -> np.ndarray:
    return np.abs(librosa.stft(audio_signal, n_fft=n_fft))


def compare_two_spectrograms(signal1: np.ndarray, signal2: np.ndarray, n_fft: int = 2048) -> float:
    spectrogram1 = calculate_spectrogram(signal1, n_fft)
    spectrogram2 = calculate_spectrogram(signal2, n_fft)
    spectrogram1, spectrogram2 = harmonize.adjust_dimensions(spectrogram1, spectrogram2)

    similarity_percentage = cosine_similarity([spectrogram1.reshape(-1)], [spectrogram2.reshape(-1)])[0][0]

    if similarity_percentage > 0.999:
        similarity_percentage = 1

    return max(0, similarity_percentage)


def compare_multiple_spectrograms(audio_signals: list, n_fft: int = 2048) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_spectrograms(audio_signals[i], audio_signals[j], n_fft)
            similarity_values.append(similarity)

    mean_similarity = np.mean(similarity_values)

    if mean_similarity > 0.999:
        mean_similarity = 1

    return mean_similarity
