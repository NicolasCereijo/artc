from core.analysis import comparisons
import numpy as np
import librosa


def calculate_harmonic_noise_ratio(audio_signal: np.ndarray, /, *, n_fft: int = 512, hop_length: int = 512) -> float:
    harmonic, _ = librosa.effects.hpss(y=audio_signal)

    harmonic_power = np.sum(np.abs(librosa.stft(harmonic, n_fft=n_fft, hop_length=hop_length))**2)
    percussive_power = np.sum(np.abs(librosa.stft(audio_signal - harmonic, n_fft=n_fft, hop_length=hop_length))**2)

    return harmonic_power / (harmonic_power + percussive_power)


def compare_two_harm_noise_ratio(audio_signal1: np.ndarray, audio_signal2: np.ndarray, /, *,
                                 n_fft: int = 512, hop_length: int = 512) -> float:
    harmonic1 = calculate_harmonic_noise_ratio(audio_signal1, n_fft=n_fft, hop_length=hop_length)
    harmonic2 = calculate_harmonic_noise_ratio(audio_signal2, n_fft=n_fft, hop_length=hop_length)

    similarity_percentage = comparisons.round_to_one(
        comparisons.normalized_relative_difference_individual(harmonic1, harmonic2))

    return max(0.0, similarity_percentage)


def compare_multiple_harm_noise_ratio(audio_signals: list, /, *, n_fft: int = 512, hop_length: int = 512) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_harm_noise_ratio(audio_signals[i], audio_signals[j],
                                                      n_fft=n_fft, hop_length=hop_length)
            similarity_values.append(similarity)

    mean_similarity = comparisons.round_to_one(np.mean(similarity_values))

    return mean_similarity
