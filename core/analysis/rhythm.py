from core.analysis import comparisons
import numpy as np
import librosa


def calculate_rhythm(audio_signal: np.ndarray, sample_rate: float, /, *, hop_length: int = 1024) -> [float, np.ndarray]:
    tempo, beat_frames = librosa.beat.beat_track(y=audio_signal, sr=sample_rate, hop_length=hop_length)
    return tempo[0], beat_frames


def compare_two_rhythm(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                       sample_rate1: float, sample_rate2: float, /, *, hop_length: int = 1024) -> float:
    tempo1, _ = calculate_rhythm(audio_signal1, sample_rate1, hop_length=hop_length)
    tempo2, _ = calculate_rhythm(audio_signal2, sample_rate2, hop_length=hop_length)

    similarity_percentage = comparisons.round_to_one(
        comparisons.normalized_relative_difference_individual(tempo1, tempo2))

    return max(0.0, similarity_percentage)


def compare_multiple_rhythm(audio_signals: list, sample_rates: list, /, *, hop_length: int = 1024) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_rhythm(audio_signals[i], audio_signals[j],
                                            sample_rates[i], sample_rates[j], hop_length=hop_length)
            similarity_values.append(similarity)

    mean_similarity = comparisons.round_to_one(np.mean(similarity_values))

    return mean_similarity
