from core.artc_collections import harmonize
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import librosa


def calculate_spectrogram(audio_signal: np.ndarray, n_fft: int = 2048) -> np.ndarray:
    """
        Calculate the spectrogram of an audio signal.

        Args:
            audio_signal (np.ndarray): The input audio signal.
            n_fft (int, optional): The number of points for the Fast Fourier Transform (FFT). Defaults to 2048.

        Returns:
            The spectrogram of the audio signal.
    """
    return np.abs(librosa.stft(audio_signal, n_fft=n_fft))


def compare_two_spectrograms(signal1: np.ndarray, signal2: np.ndarray) -> float:
    spectrogram1 = calculate_spectrogram(signal1)
    spectrogram2 = calculate_spectrogram(signal2)
    spectrogram1, spectrogram2 = harmonize.adjust_dimensions(spectrogram1, spectrogram2)

    similarity_percentage = cosine_similarity([spectrogram1.reshape(-1)], [spectrogram2.reshape(-1)])[0][0]
    if similarity_percentage > 0.999:
        similarity_percentage = 1

    return max(0, similarity_percentage)


def compare_multiple_spectrograms(*audio_signals: np.ndarray[float, ...]) -> float:
    spectrograms = map(lambda signal: calculate_spectrogram(signal), audio_signals)
    spectrograms = harmonize.adjust_dimensions(*spectrograms)
    results = []

    for i in range(0, len(spectrograms) - 1):
        for j in range(i + 1, len(spectrograms)):
            results.append(max(0, cosine_similarity([spectrograms[i]], [spectrograms[j]])[0][0]))

    return sum(results) / len(results)
