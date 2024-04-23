from core.artc_collections import harmonize
import numpy as np
import librosa


def calculate_energy_envelope(audio_signal: np.ndarray, hop_length: int = 2048) -> np.ndarray:
    return librosa.feature.rms(y=audio_signal, hop_length=hop_length)


def compare_two_energy_envelope(audio_signal1: np.ndarray, audio_signal2: np.ndarray, hop_length: int = 2048) -> float:
    energy_envelope1 = calculate_energy_envelope(audio_signal1, hop_length)
    energy_envelope2 = calculate_energy_envelope(audio_signal2, hop_length)

    e_envelope1_vector, e_envelope2_vector = harmonize.adjust_dimensions(energy_envelope1, energy_envelope2)
    correlation = np.corrcoef(e_envelope1_vector.flatten(), e_envelope2_vector.flatten())[0, 1]

    similarity_percentage = (correlation + 1) / 2

    if similarity_percentage > 0.999:
        similarity_percentage = 1

    return similarity_percentage


def compare_multiple_energy_envelope(audio_signals: list, hop_length: int = 2048) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_energy_envelope(audio_signals[i], audio_signals[j], hop_length)
            similarity_values.append(similarity)

    mean_similarity = np.mean(similarity_values)

    if mean_similarity > 0.999:
        mean_similarity = 1

    return mean_similarity
