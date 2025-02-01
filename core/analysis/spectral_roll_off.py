import numpy as np
from librosa.feature import spectral_rolloff


def calculate_spectral_roll_off(audio_signal: np.ndarray, sample_rate: float,
                                /, *, n_fft: int = 512, roll_percent: float = 0.5) -> np.ndarray:
    roll_off = spectral_rolloff(y=audio_signal, sr=sample_rate,
                                n_fft=n_fft, roll_percent=roll_percent)
    return np.fft.fft(roll_off)


def compare_two_spectral_roll_off(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                                  sample_rate1: float, sample_rate2: float,
                                  /, *, n_fft: int = 512, roll_percent: float = 0.5) -> float:
    roll_off_1 = calculate_spectral_roll_off(
        audio_signal1, sample_rate1, n_fft=n_fft, roll_percent=roll_percent)
    roll_off_2 = calculate_spectral_roll_off(
        audio_signal2, sample_rate2, n_fft=n_fft, roll_percent=roll_percent)

    min_len = min(roll_off_1.shape[1], roll_off_2.shape[1])
    roll_off_1_adjusted = roll_off_1[:, :min_len]
    roll_off_2_adjusted = roll_off_2[:, :min_len]

    distance = np.linalg.norm(np.abs(roll_off_1_adjusted) -
                              np.abs(roll_off_2_adjusted))
    max_distance = (np.linalg.norm(np.abs(roll_off_1_adjusted)) +
                    np.linalg.norm(np.abs(roll_off_2_adjusted)))

    similarity = (1 - distance / max_distance) if max_distance > 0 else 1.0
    return float(similarity)


def compare_multiple_spectral_roll_off(audio_signals: list, sample_rates: list,
                                       /, *, n_fft: int = 512, roll_percent: float = 0.5) -> float:
    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_spectral_roll_off(
                audio_signals[i], audio_signals[j],
                sample_rates[i], sample_rates[j],
                n_fft=n_fft, roll_percent=roll_percent
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
