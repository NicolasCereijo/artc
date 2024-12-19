import numpy as np
import librosa


def calculate_peak_matching(audio_signal: np.ndarray, sample_rate: float,
                            /, *, n_fft: int = 4096) -> [np.ndarray, np.ndarray]:
    spectrogram = np.abs(librosa.stft(audio_signal, n_fft=n_fft))
    one_dimensional_spectrogram = np.mean(spectrogram, axis=1)

    """
        - pre_max (typical range: 3-10): Number of samples before the current point that must be
        smaller for it to be considered a peak.
        - post_max (typical range: 3-10): Number of samples after the current point that must be
        smaller for it to be considered a peak.
        - pre_avg (typical range: 3-10): Number of samples before the current point to compute the
        local average, helping to smooth the signal.
        - post_avg (typical range: 3-10): Number of samples after the current point to compute the
        local average, helping to smooth the signal.
        - delta (typical range: 0.1-1.0): Minimum amplitude threshold that a peak must have to be
        considered as such, detecting only the most prominent peaks.
        - wait (typical range: 1-10): Minimum number of samples between successive peaks, preventing
        the detection of peaks that are too close to each other.
    """
    spectral_peaks = librosa.util.peak_pick(
        librosa.amplitude_to_db(one_dimensional_spectrogram),
        pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=0.5, wait=5)

    fft_frequencies = librosa.core.fft_frequencies(sr=sample_rate, n_fft=n_fft)
    peak_frequencies = fft_frequencies[spectral_peaks]
    peak_magnitudes = one_dimensional_spectrogram[spectral_peaks]

    return peak_frequencies, peak_magnitudes


def compare_two_peak_matching(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                              sample_rate1: float, sample_rate2: float,
                              /, *, n_fft: int = 4096) -> float:
    peak_freq1, peak_mag1 = calculate_peak_matching(audio_signal1, sample_rate1, n_fft=n_fft)
    peak_freq2, peak_mag2 = calculate_peak_matching(audio_signal2, sample_rate2, n_fft=n_fft)

    min_len_freq = min(len(peak_freq1), len(peak_freq2))
    min_len_mag = min(len(peak_mag1), len(peak_mag2))
    peak_freq1_adjusted = peak_freq1[:min_len_freq]
    peak_freq2_adjusted = peak_freq2[:min_len_freq]
    peak_mag1_adjusted = peak_mag1[:min_len_mag]
    peak_mag2_adjusted = peak_mag2[:min_len_mag]

    distance_freq = np.linalg.norm(np.abs(peak_freq1_adjusted - peak_freq2_adjusted))
    max_distance_freq = (np.linalg.norm(np.abs(peak_freq1_adjusted)) +
                         np.linalg.norm(np.abs(peak_freq2_adjusted)))
    distance_mag = np.linalg.norm(np.abs(peak_mag1_adjusted - peak_mag2_adjusted))
    max_distance_mag = (np.linalg.norm(np.abs(peak_mag1_adjusted)) +
                        np.linalg.norm(np.abs(peak_mag2_adjusted)))

    similarity_freq = (1 - distance_freq / max_distance_freq) if max_distance_freq > 0 else 1.0
    similarity_mag = (1 - distance_mag / max_distance_mag) if max_distance_mag > 0 else 1.0

    similarity = (similarity_freq + similarity_mag) / 2
    return similarity


def compare_multiple_peak_matching(audio_signals: list, sample_rates: list,
                                   /, *, n_fft: int = 4096) -> float:
    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    num_signals = len(audio_signals)
    total_similarity = 0.0
    num_comparisons = 0

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            total_similarity += compare_two_peak_matching(
                audio_signals[i], audio_signals[j],
                sample_rates[i], sample_rates[j],
                n_fft=n_fft
            )
            num_comparisons += 1

    return total_similarity / num_comparisons if num_comparisons > 0 else 0.0
