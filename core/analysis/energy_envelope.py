import numpy as np
from librosa.feature import rms


def calculate_energy_envelope(audio_signal: np.ndarray,
                              /, *, hop_length: int = 512) -> np.ndarray:
    energy_envelope = rms(y=audio_signal, hop_length=hop_length)
    return np.fft.fft(energy_envelope)


def compare_two_energy_envelope(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                                /, *, hop_length: int = 512) -> float:
    energy_envelope1 = calculate_energy_envelope(audio_signal1, hop_length=hop_length)
    energy_envelope2 = calculate_energy_envelope(audio_signal2, hop_length=hop_length)

    min_len = min(energy_envelope1.shape[1], energy_envelope2.shape[1])
    energy1_adjusted = energy_envelope1[:, :min_len]
    energy2_adjusted = energy_envelope2[:, :min_len]

    distance = np.linalg.norm(energy1_adjusted - energy2_adjusted)
    max_distance = (np.linalg.norm(energy1_adjusted) +
                    np.linalg.norm(energy2_adjusted))

    similarity = (1 - distance / max_distance) if max_distance > 0 else 1.0
    return float(similarity)


def compare_multiple_energy_envelope(audio_signals: list,
                                     /, *, hop_length: int = 512) -> float:
    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_energy_envelope(
                audio_signals[i], audio_signals[j],
                hop_length=hop_length
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
