from core.artc_collections import harmonize
import numpy as np
import librosa
from sklearn.metrics.pairwise import cosine_similarity


def calculate_mfcc(audio_signal: np.ndarray, sample_rate: float, n_fft: int = 8192) -> np.ndarray:
    mfcc = librosa.feature.mfcc(y=audio_signal, sr=sample_rate, n_mfcc=13, n_fft=n_fft)
    return mfcc


def compare_two_mfcc(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                     sample_rate1: float, sample_rate2: float, n_fft: int = 8192) -> np.float32:
    mfcc1 = calculate_mfcc(audio_signal1, sample_rate1, n_fft)
    mfcc2 = calculate_mfcc(audio_signal2, sample_rate2, n_fft)

    mfcc1_vector, mfcc2_vector = harmonize.adjust_dimensions(mfcc1, mfcc2)

    similarity_percentage = cosine_similarity(mfcc1_vector, mfcc2_vector)[0][0]

    if similarity_percentage > 0.999:
        similarity_percentage = 1

    return similarity_percentage
