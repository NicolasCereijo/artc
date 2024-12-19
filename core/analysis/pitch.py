import numpy as np
from librosa.core import piptrack


def calculate_pitch(audio_signal: np.ndarray, sample_rate: float,
                    /, *, n_fft: int = 8192) -> np.ndarray:
    pitches, magnitudes = piptrack(y=audio_signal, sr=sample_rate, n_fft=n_fft)
    return np.fft.fft(pitches[magnitudes.argmax(axis=0), np.arange(magnitudes.shape[1])])


def compare_two_pitch(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                      sample_rate1: float, sample_rate2: float,
                      /, *, n_fft: int = 8192) -> float:
    pitch1 = calculate_pitch(audio_signal1, sample_rate1, n_fft=n_fft)
    pitch2 = calculate_pitch(audio_signal2, sample_rate2, n_fft=n_fft)

    min_len = min(len(pitch1), len(pitch2))
    pitch1_adjusted = pitch1[:min_len]
    pitch2_adjusted = pitch2[:min_len]

    distance = np.linalg.norm(pitch1_adjusted - pitch2_adjusted)
    max_distance = (np.linalg.norm(pitch1_adjusted) +
                    np.linalg.norm(pitch2_adjusted))

    similarity = (1 - distance / max_distance) if max_distance > 0 else 1.0
    return max(0.0, similarity)


def compare_multiple_pitch(audio_signals: list, sample_rates: list,
                           /, *, n_fft: int = 8192) -> float:
    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_pitch(
                audio_signals[i], audio_signals[j],
                sample_rates[i], sample_rates[j],
                n_fft=n_fft
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
