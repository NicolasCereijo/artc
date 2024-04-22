import numpy as np
import librosa


def calculate_rhythm(audio_signal: np.ndarray, sample_rate: float, hop_length: int = 1024) -> [np.float64, np.ndarray]:
    tempo, beat_frames = librosa.beat.beat_track(y=audio_signal, sr=sample_rate, hop_length=hop_length)
    return tempo, beat_frames


def compare_two_rhythm(audio_signal1: np.ndarray, audio_signal2: np.ndarray,
                       sample_rate1: float, sample_rate2: float, hop_length: int = 1024) -> float:
    tempo1, _ = calculate_rhythm(audio_signal1, sample_rate1, hop_length)
    tempo2, _ = calculate_rhythm(audio_signal2, sample_rate2, hop_length)

    similarity_percentage = 1 - (abs(tempo1 - tempo2) / max(tempo1, tempo2))

    if similarity_percentage > 0.999:
        similarity_percentage = 1

    return similarity_percentage
