import librosa
import pytest
from pathlib import Path

import core.analysis as analysis


@pytest.fixture()
def setup():
    current_path = Path(__file__)

    if current_path.parent.name == 'test_analysis':
        data_path = current_path.parent.parent / 'fixtures'
    elif current_path.parent.name == 'tests':
        data_path = current_path.parent / 'fixtures'
    else:
        data_path = current_path.parent / 'tests' / 'fixtures'

    data_set = {"individual_files":  [
        {"path": data_path, "name": "little-waves.mp3"},
        {"path": data_path, "name": "waves-in-caves.wav"},
        {"path": data_path, "name": "Water Sizzle.mp3"}
    ]}

    return data_set


def test_compare_two_harm_noise_ratio(setup):
    data_set = setup
    n_fft = 512
    hop_length: int = 512
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] /
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] /
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] /
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_two_harm_noise_ratio(audio_signal1, audio_signal1, n_fft=n_fft,
                                                 hop_length=hop_length) == 1
    assert analysis.compare_two_harm_noise_ratio(audio_signal2, audio_signal2, n_fft=n_fft,
                                                 hop_length=hop_length) == 1
    assert analysis.compare_two_harm_noise_ratio(audio_signal3, audio_signal3, n_fft=n_fft,
                                                 hop_length=hop_length) == 1
    assert round(analysis.compare_two_harm_noise_ratio(audio_signal1, audio_signal2, n_fft=n_fft,
                                                       hop_length=hop_length), 5) == 0.73186
    assert round(analysis.compare_two_harm_noise_ratio(audio_signal2, audio_signal1, n_fft=n_fft,
                                                       hop_length=hop_length), 5) == 0.73186
    assert round(analysis.compare_two_harm_noise_ratio(audio_signal1, audio_signal3, n_fft=n_fft,
                                                       hop_length=hop_length), 5) == 0.42965
    assert round(analysis.compare_two_harm_noise_ratio(audio_signal3, audio_signal1, n_fft=n_fft,
                                                       hop_length=hop_length), 5) == 0.42965
    assert round(analysis.compare_two_harm_noise_ratio(audio_signal2, audio_signal3, n_fft=n_fft,
                                                       hop_length=hop_length), 5) == 0.58707
    assert round(analysis.compare_two_harm_noise_ratio(audio_signal3, audio_signal2, n_fft=n_fft,
                                                       hop_length=hop_length), 5) == 0.58707


def test_compare_multiple_harm_noise_ratio(setup):
    data_set = setup
    n_fft = 512
    hop_length: int = 512
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] /
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] /
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] /
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_multiple_harm_noise_ratio([audio_signal1, audio_signal1],
                                                      n_fft=n_fft,
                                                      hop_length=hop_length) == 1
    assert analysis.compare_multiple_harm_noise_ratio([audio_signal2, audio_signal2],
                                                      n_fft=n_fft,
                                                      hop_length=hop_length) == 1
    assert analysis.compare_multiple_harm_noise_ratio([audio_signal3, audio_signal3],
                                                      n_fft=n_fft,
                                                      hop_length=hop_length) == 1
    assert round(analysis.compare_multiple_harm_noise_ratio([audio_signal1, audio_signal2],
                                                            n_fft=n_fft,
                                                            hop_length=hop_length), 5) == 0.73186
    assert round(analysis.compare_multiple_harm_noise_ratio([audio_signal2, audio_signal1],
                                                            n_fft=n_fft,
                                                            hop_length=hop_length), 5) == 0.73186
    assert round(analysis.compare_multiple_harm_noise_ratio([audio_signal1, audio_signal3],
                                                            n_fft=n_fft,
                                                            hop_length=hop_length), 5) == 0.42965
    assert round(analysis.compare_multiple_harm_noise_ratio([audio_signal3, audio_signal1],
                                                            n_fft=n_fft,
                                                            hop_length=hop_length), 5) == 0.42965
    assert round(analysis.compare_multiple_harm_noise_ratio([audio_signal2, audio_signal3],
                                                            n_fft=n_fft,
                                                            hop_length=hop_length), 5) == 0.58707
    assert round(analysis.compare_multiple_harm_noise_ratio([audio_signal3, audio_signal2],
                                                            n_fft=n_fft,
                                                            hop_length=hop_length), 5) == 0.58707

    assert analysis.compare_multiple_harm_noise_ratio([audio_signal1, audio_signal1, audio_signal1],
                                                      n_fft=n_fft,
                                                      hop_length=hop_length) == 1
    assert analysis.compare_multiple_harm_noise_ratio([audio_signal2, audio_signal2, audio_signal2],
                                                      n_fft=n_fft,
                                                      hop_length=hop_length) == 1
    assert analysis.compare_multiple_harm_noise_ratio([audio_signal3, audio_signal3, audio_signal3],
                                                      n_fft=n_fft,
                                                      hop_length=hop_length) == 1
