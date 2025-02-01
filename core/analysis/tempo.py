import numpy as np
from librosa.beat import beat_track


def calculate_tempo(audio_signal: np.ndarray, sample_rate: float,
                    /, *, hop_length: int = 1024) -> float:
    tempo, _ = beat_track(y=audio_signal, sr=sample_rate, hop_length=hop_length)

    if isinstance(tempo, np.ndarray):
        tempo = np.mean(tempo)
    return float(tempo)


def compare_two_tempo(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                      sample_rate1: float, sample_rate2: float,
                      /, *, hop_length: int = 1024) -> float:
    tempo1 = calculate_tempo(audio_signal1, sample_rate1, hop_length=hop_length)
    tempo2 = calculate_tempo(audio_signal2, sample_rate2, hop_length=hop_length)

    distance = abs(tempo1 - tempo2)
    max_distance = max(tempo1, tempo2)

    similarity = (1 - distance / max_distance) if max_distance > 0 else 1.0
    return max(0.0, similarity)


def compare_multiple_tempo(audio_signals: list, sample_rates: list,
                           /, *, hop_length: int = 1024) -> float:
    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_tempo(
                audio_signals[i], audio_signals[j],
                sample_rates[i], sample_rates[j],
                hop_length=hop_length
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
