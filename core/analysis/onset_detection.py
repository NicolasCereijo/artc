import numpy as np
from librosa.onset import onset_strength


def calculate_onset_detection(audio_signal: np.ndarray, sample_rate: float,
                              /, *, hop_length: int = 8192) -> np.ndarray:
    return onset_strength(y=audio_signal, sr=sample_rate, hop_length=hop_length)


def compare_two_onset_detection(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                                sample_rate1: float, sample_rate2: float,
                                /, *, hop_length: int = 8192) -> float:
    onset_env1 = calculate_onset_detection(audio_signal1, sample_rate1, hop_length=hop_length)
    onset_env2 = calculate_onset_detection(audio_signal2, sample_rate2, hop_length=hop_length)

    min_len = min(onset_env1.shape[0], onset_env2.shape[0])
    onset_env1_adjusted = onset_env1[:min_len]
    onset_env2_adjusted = onset_env2[:min_len]

    distance = np.linalg.norm(onset_env1_adjusted - onset_env2_adjusted)
    max_distance = (np.linalg.norm(onset_env1_adjusted) +
                    np.linalg.norm(onset_env2_adjusted))

    similarity = (1 - distance / max_distance) if max_distance > 0 else 1.0
    return similarity


def compare_multiple_onset_detection(audio_signals: list, sample_rates: list,
                                     /, *, hop_length: int = 8192) -> float:
    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_onset_detection(
                audio_signals[i], audio_signals[j],
                sample_rates[i], sample_rates[j],
                hop_length=hop_length
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
