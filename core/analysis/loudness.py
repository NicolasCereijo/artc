import numpy as np
import librosa


def calculate_loudness(audio_signal: np.ndarray, sample_rate: float) -> np.ndarray:
    magnitude_spectrogram = np.abs(librosa.stft(audio_signal))
    db_spectrogram = librosa.amplitude_to_db(magnitude_spectrogram, ref=np.max)

    frequencies = librosa.fft_frequencies(sr=sample_rate)
    frequencies[frequencies == 0] = 1e-6  # Avoid log10(0)

    weighting = librosa.A_weighting(frequencies)[:, np.newaxis]
    return np.fft.fft(db_spectrogram * weighting)


def compare_two_loudness(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                         sample_rate1: float, sample_rate2: float, /) -> float:
    loudness1 = calculate_loudness(audio_signal1, sample_rate1)
    loudness2 = calculate_loudness(audio_signal2, sample_rate2)

    min_len = min(loudness1.shape[1], loudness2.shape[1])
    loudness1_adjusted = loudness1[:, :min_len]
    loudness2_adjusted = loudness2[:, :min_len]

    distance = np.linalg.norm(loudness1_adjusted - loudness2_adjusted)
    max_distance = (np.linalg.norm(loudness1_adjusted) +
                    np.linalg.norm(loudness2_adjusted))

    similarity = (1 - distance / max_distance) if max_distance > 0 else 1.0
    return float(similarity)


def compare_multiple_loudness(audio_signals: list, sample_rates: list, /) -> float:
    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_loudness(
                audio_signals[i], audio_signals[j],
                sample_rates[i], sample_rates[j]
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
