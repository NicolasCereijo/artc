from core.analysis import comparisons
import numpy as np
import librosa


def calculate_chroma(audio_signal: np.ndarray, sample_rate: float, n_fft: int = 2048) -> np.ndarray:
    return librosa.feature.chroma_stft(y=audio_signal, sr=sample_rate, n_fft=n_fft)


def compare_two_chroma(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                       sample_rate1: float, sample_rate2: float, n_fft: int = 2048) -> float:
    chroma1 = calculate_chroma(audio_signal1, sample_rate1, n_fft)
    chroma2 = calculate_chroma(audio_signal2, sample_rate2, n_fft)

    similarity_percentage = comparisons.pearson_correlation(chroma1, chroma2)

    if similarity_percentage > 0.999:
        similarity_percentage = 1

    return similarity_percentage


def compare_multiple_chroma(audio_signals: list, sample_rates: list, n_fft: int = 2048) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_chroma(audio_signals[i], audio_signals[j],
                                            sample_rates[i], sample_rates[j], n_fft)
            similarity_values.append(similarity)

    mean_similarity = np.mean(similarity_values)

    if mean_similarity > 0.999:
        mean_similarity = 1

    return mean_similarity
