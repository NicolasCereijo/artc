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
