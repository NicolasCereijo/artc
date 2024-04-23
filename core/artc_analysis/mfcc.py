from core.artc_collections import harmonize
import numpy as np
import librosa
from sklearn.metrics.pairwise import cosine_similarity


def calculate_mfcc(audio_signal: np.ndarray, sample_rate: float, n_fft: int = 8192) -> np.ndarray:
    mfcc = librosa.feature.mfcc(y=audio_signal, sr=sample_rate, n_mfcc=13, n_fft=n_fft)
    return mfcc


def compare_two_mfcc(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                     sample_rate1: float, sample_rate2: float, n_fft: int = 8192) -> float:
    mfcc1 = calculate_mfcc(audio_signal1, sample_rate1, n_fft)
    mfcc2 = calculate_mfcc(audio_signal2, sample_rate2, n_fft)

    mfcc1_vector, mfcc2_vector = harmonize.adjust_dimensions(mfcc1, mfcc2)

    similarity_percentage = cosine_similarity(mfcc1_vector, mfcc2_vector)[0][0]

    if similarity_percentage > 0.999:
        similarity_percentage = 1

    return similarity_percentage


def compare_multiple_mfcc(audio_signals: list, sample_rates: list, n_fft: int = 8192) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_mfcc(audio_signals[i], audio_signals[j],
                                          sample_rates[i], sample_rates[j], n_fft)
            similarity_values.append(similarity)

    mean_similarity = np.mean(similarity_values)

    if mean_similarity > 0.999:
        mean_similarity = 1

    return mean_similarity
