from core.artc_collections import harmonize
import numpy as np
import librosa


def calculate_chroma(audio_signal: np.ndarray, sample_rate: float, n_fft: int = 2048) -> np.ndarray:
    return librosa.feature.chroma_stft(y=audio_signal, sr=sample_rate, n_fft=n_fft)


def compare_two_chroma(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                       sample_rate1: float, sample_rate2: float, n_fft: int = 2048) -> float:
    chroma1 = calculate_chroma(audio_signal1, sample_rate1, n_fft)
    chroma2 = calculate_chroma(audio_signal2, sample_rate2, n_fft)

    harmonize.adjust_length(chroma1, chroma2)
    chroma1_vector, chroma2_vector = harmonize.adjust_dimensions(chroma1, chroma2)

    correlation = np.corrcoef(chroma1_vector.flatten(), chroma2_vector.flatten())[0, 1]
    similarity_percentage = (correlation + 1) / 2

    if similarity_percentage > 0.999:
        similarity_percentage = 1

    return similarity_percentage
