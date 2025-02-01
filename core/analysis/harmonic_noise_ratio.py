import numpy as np
from librosa import stft
from librosa.effects import hpss


def calculate_harmonic_noise_ratio(audio_signal: np.ndarray,
                                   /, *, n_fft: int = 512, hop_length: int = 512) -> float:
    harmonic, percussive = hpss(y=audio_signal)

    harmonic_power = np.sum(np.abs(stft(harmonic, n_fft=n_fft, hop_length=hop_length))**2)
    percussive_power = np.sum(np.abs(stft(percussive, n_fft=n_fft, hop_length=hop_length))**2)

    total_power = harmonic_power + percussive_power
    return float(harmonic_power / total_power if total_power > 0 else 0.0)


def compare_two_hnr(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                    /, *, n_fft: int = 512, hop_length: int = 512) -> float:
    hnr1 = calculate_harmonic_noise_ratio(audio_signal1, n_fft=n_fft, hop_length=hop_length)
    hnr2 = calculate_harmonic_noise_ratio(audio_signal2, n_fft=n_fft, hop_length=hop_length)

    distance = abs(hnr1 - hnr2)
    max_distance = max(abs(hnr1), abs(hnr2))

    similarity = (1 - distance / max_distance) if max_distance > 0 else 1.0
    return similarity


def compare_multiple_hnr(audio_signals: list,
                         /, *, n_fft: int = 512, hop_length: int = 512) -> float:
    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_hnr(
                audio_signals[i], audio_signals[j],
                n_fft=n_fft, hop_length=hop_length
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
