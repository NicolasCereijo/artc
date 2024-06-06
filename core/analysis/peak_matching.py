from core.analysis import comparisons
import numpy as np
import librosa


def calculate_peak_matching(audio_signal: np.ndarray, sample_rate: float,
                            n_fft: int = 4096) -> [np.ndarray, np.ndarray]:
    spectrogram = np.abs(librosa.stft(audio_signal, n_fft=n_fft))
    one_dimensional_spectrogram = np.mean(spectrogram, axis=1)

    """
        - pre_max (typical range: 3-10): Number of samples before the current point that must be smaller for it to be
        considered a peak.
        - post_max (typical range: 3-10): Number of samples after the current point that must be smaller for it to be
        considered a peak.
        - pre_avg (typical range: 3-10): Number of samples before the current point to compute the local average,
        helping to smooth the signal.
        - post_avg (typical range: 3-10): Number of samples after the current point to compute the local average,
        helping to smooth the signal.
        - delta (typical range: 0.1-1.0): Minimum amplitude threshold that a peak must have to be considered as such,
        detecting only the most prominent peaks.
        - wait (typical range: 1-10): Minimum number of samples between successive peaks, preventing the detection of
        peaks that are too close to each other.
    """
    spectral_peaks = librosa.util.peak_pick(librosa.amplitude_to_db(one_dimensional_spectrogram),
                                            pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=0.5, wait=5)

    fft_frequencies = librosa.core.fft_frequencies(sr=sample_rate, n_fft=n_fft)
    peak_frequencies = fft_frequencies[spectral_peaks]

    peak_magnitudes = one_dimensional_spectrogram[spectral_peaks]
    return peak_frequencies, peak_magnitudes


def compare_two_peak_matching(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                              sample_rate1: float, sample_rate2: float, n_fft: int = 4096) -> float:
    peak_freq1, peak_mag1 = calculate_peak_matching(audio_signal1, sample_rate1, n_fft)
    peak_freq2, peak_mag2 = calculate_peak_matching(audio_signal2, sample_rate2, n_fft)

    similarity_percentage_peak_freq = comparisons.round_to_one(
        comparisons.normalized_relative_difference_array(peak_freq1, peak_freq2))
    similarity_percentage_peak_mag = comparisons.round_to_one(
        comparisons.normalized_relative_difference_array(peak_mag1, peak_mag2))

    similarity_percentage = (similarity_percentage_peak_freq + similarity_percentage_peak_mag) / 2

    return max(0.0, similarity_percentage)


def compare_multiple_peak_matching(audio_signals: list, sample_rates: list, n_fft: int = 4096) -> float:
    num_signals = len(audio_signals)
    similarity_values = []

    if len(audio_signals) != len(sample_rates):
        raise ValueError("The number of signals must match the number of sampling rates")

    for i in range(num_signals):
        for j in range(i + 1, num_signals):
            similarity = compare_two_peak_matching(audio_signals[i], audio_signals[j],
                                                   sample_rates[i], sample_rates[j], n_fft)
            similarity_values.append(similarity)

    mean_similarity = comparisons.round_to_one(np.mean(similarity_values))

    return mean_similarity
