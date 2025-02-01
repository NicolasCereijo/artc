import numpy as np
from librosa.feature import chroma_cens


def calculate_chroma_cens(audio_signal: np.ndarray, sample_rate: float,
                          /, *, hop_length: int = 512) -> np.ndarray:
    chr_cens = chroma_cens(y=audio_signal, sr=sample_rate, hop_length=hop_length)
    return np.fft.fft(chr_cens)


def compare_two_chroma_cens(signal1: np.ndarray, signal2: np.ndarray,
                            sample_rate1: float, sample_rate2: float,
                            /, *, hop_length: int = 512) -> float:
    chroma_cens1 = calculate_chroma_cens(signal1, sample_rate1, hop_length=hop_length)
    chroma_cens2 = calculate_chroma_cens(signal2, sample_rate2, hop_length=hop_length)

    min_len = min(chroma_cens1.shape[1], chroma_cens2.shape[1])
    chroma_cens1_adjusted = chroma_cens1[:, :min_len]
    chroma_cens2_adjusted = chroma_cens2[:, :min_len]

    distance = np.linalg.norm(np.abs(chroma_cens1_adjusted) -
                              np.abs(chroma_cens2_adjusted))
    max_distance = (np.linalg.norm(np.abs(chroma_cens1_adjusted)) +
                    np.linalg.norm(np.abs(chroma_cens2_adjusted)))

    similarity = (1 - distance / max_distance) if max_distance > 0 else 1.0
    return float(similarity)


def compare_multiple_chroma_cens(audio_signals: list, sample_rates: list,
                                 /, *, hop_length: int = 512) -> float:
    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_chroma_cens(
                audio_signals[i], audio_signals[j],
                sample_rates[i], sample_rates[j],
                hop_length=hop_length
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
