import numpy as np
from librosa.feature import spectral_flatness


def calculate_spectral_flatness(audio_signal: np.ndarray,
                                /, *, n_fft: int = 8192) -> np.ndarray:
    return np.fft.fft(spectral_flatness(y=audio_signal, n_fft=n_fft))


def compare_two_spectral_flatness(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                                  /, *, n_fft: int = 8192) -> float:
    flatness_1 = calculate_spectral_flatness(audio_signal1, n_fft=n_fft)
    flatness_2 = calculate_spectral_flatness(audio_signal2, n_fft=n_fft)

    min_len = min(flatness_1.shape[1], flatness_2.shape[1])
    flatness_1_adjusted = flatness_1[:, :min_len]
    flatness_2_adjusted = flatness_2[:, :min_len]

    distance = np.linalg.norm(np.abs(flatness_1_adjusted) -
                              np.abs(flatness_2_adjusted))
    max_distance = (np.linalg.norm(np.abs(flatness_1_adjusted)) +
                    np.linalg.norm(np.abs(flatness_2_adjusted)))

    similarity = (1 - distance / max_distance) if max_distance > 0 else 1.0
    return float(similarity)


def compare_multiple_spectral_flatness(audio_signals: list,
                                       /, *, n_fft: int = 8192) -> float:
    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_spectral_flatness(
                audio_signals[i], audio_signals[j],
                n_fft=n_fft
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
