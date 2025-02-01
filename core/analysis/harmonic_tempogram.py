import numpy as np
from librosa.feature import tempogram
from librosa.onset import onset_strength


def calculate_harmonic_tempogram(audio_signal: np.ndarray, sample_rate: float,
                                 /, *, hop_length: int = 512) -> np.ndarray:
    harmonic_tempogram = tempogram(y=audio_signal, sr=sample_rate, hop_length=hop_length,
                                   onset_envelope=onset_strength(y=audio_signal, sr=sample_rate))
    return np.fft.fft(harmonic_tempogram)


def compare_two_harmonic_tempogram(signal1: np.ndarray, signal2: np.ndarray,
                                   sample_rate1: float, sample_rate2: float,
                                   /, *, hop_length: int = 512) -> float:
    harmonic_tempogram1 = calculate_harmonic_tempogram(signal1, sample_rate1, hop_length=hop_length)
    harmonic_tempogram2 = calculate_harmonic_tempogram(signal2, sample_rate2, hop_length=hop_length)

    min_len = min(harmonic_tempogram1.shape[1], harmonic_tempogram2.shape[1])
    harmonic_tempogram1_adjusted = harmonic_tempogram1[:, :min_len]
    harmonic_tempogram2_adjusted = harmonic_tempogram2[:, :min_len]

    distance = np.linalg.norm(np.abs(harmonic_tempogram1_adjusted) -
                              np.abs(harmonic_tempogram2_adjusted))
    max_distance = (np.linalg.norm(np.abs(harmonic_tempogram1_adjusted)) +
                    np.linalg.norm(np.abs(harmonic_tempogram2_adjusted)))

    similarity = (1 - distance / max_distance) if max_distance > 0 else 1.0
    return float(similarity)


def compare_multiple_harmonic_tempogram(audio_signals: list, sample_rates: list,
                                        /, *, hop_length: int = 512) -> float:
    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_harmonic_tempogram(
                audio_signals[i], audio_signals[j],
                sample_rates[i], sample_rates[j],
                hop_length=hop_length
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
