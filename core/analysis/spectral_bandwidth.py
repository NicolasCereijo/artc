import numpy as np
from librosa.feature import spectral_bandwidth


def calculate_spectral_bandwidth(audio_signal: np.ndarray, sample_rate: float,
                                 /, *, n_fft: int = 4096) -> np.ndarray:
    return np.fft.fft(spectral_bandwidth(y=audio_signal, sr=sample_rate, n_fft=n_fft))


def compare_two_spectral_bandwidth(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                                   sample_rate1: float, sample_rate2: float,
                                   /, *, n_fft: int = 4096) -> float:
    bandwidth_1 = calculate_spectral_bandwidth(audio_signal1, sample_rate1, n_fft=n_fft)
    bandwidth_2 = calculate_spectral_bandwidth(audio_signal2, sample_rate2, n_fft=n_fft)

    min_len = min(bandwidth_1.shape[1], bandwidth_2.shape[1])
    bandwidth_1_adjusted = bandwidth_1[:, :min_len]
    bandwidth_2_adjusted = bandwidth_2[:, :min_len]

    distance = np.linalg.norm(np.abs(bandwidth_1_adjusted) -
                              np.abs(bandwidth_2_adjusted))
    max_distance = (np.linalg.norm(np.abs(bandwidth_1_adjusted)) +
                    np.linalg.norm(np.abs(bandwidth_2_adjusted)))

    similarity = (1 - distance / max_distance) if max_distance > 0 else 1.0
    return similarity


def compare_multiple_spectral_bandwidth(audio_signals: list, sample_rates: list,
                                        /, *, n_fft: int = 4096) -> float:
    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_spectral_bandwidth(
                audio_signals[i], audio_signals[j],
                sample_rates[i], sample_rates[j],
                n_fft=n_fft
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
