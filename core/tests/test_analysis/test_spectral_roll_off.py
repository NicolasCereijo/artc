import core.analysis as analysis
import importlib.resources
import librosa
import pytest


@pytest.fixture()
def setup():
    files_path = str(importlib.resources.path('test_collection.water_sounds', '')) + '/'

    data_set = {"individual_files":  [
        {"path": files_path, "name": "little-waves.mp3"},
        {"path": files_path, "name": "waves-in-caves.wav"},
        {"path": files_path, "name": "Water Sizzle.mp3"}
    ]}

    return data_set


def test_compare_two_spectral_roll_off(setup):
    data_set = setup
    n_fft = 512
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] +
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] +
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] +
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_two_spectral_roll_off(audio_signal1, audio_signal1,
                                                  sample_rate1, sample_rate1, n_fft=n_fft) == 1
    assert analysis.compare_two_spectral_roll_off(audio_signal2, audio_signal2,
                                                  sample_rate2, sample_rate2, n_fft=n_fft) == 1
    assert analysis.compare_two_spectral_roll_off(audio_signal3, audio_signal3,
                                                  sample_rate3, sample_rate3, n_fft=n_fft) == 1
    assert analysis.compare_two_spectral_roll_off(audio_signal1, audio_signal2,
                                                  sample_rate1, sample_rate2, n_fft=n_fft) == 0.8707927973098482
    assert analysis.compare_two_spectral_roll_off(audio_signal2, audio_signal1,
                                                  sample_rate2, sample_rate1, n_fft=n_fft) == 0.8707927973098482
    assert analysis.compare_two_spectral_roll_off(audio_signal1, audio_signal3,
                                                  sample_rate1, sample_rate3, n_fft=n_fft) == 0.8751719403368576
    assert analysis.compare_two_spectral_roll_off(audio_signal3, audio_signal1,
                                                  sample_rate3, sample_rate1, n_fft=n_fft) == 0.8751719403368576
    assert analysis.compare_two_spectral_roll_off(audio_signal2, audio_signal3,
                                                  sample_rate2, sample_rate3, n_fft=n_fft) == 0.994996248365408
    assert analysis.compare_two_spectral_roll_off(audio_signal3, audio_signal2,
                                                  sample_rate3, sample_rate2, n_fft=n_fft) == 0.994996248365408


def test_compare_multiple_spectral_roll_off(setup):
    data_set = setup
    n_fft = 512
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] +
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] +
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] +
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_multiple_spectral_roll_off([audio_signal1, audio_signal1],
                                                       [sample_rate1, sample_rate1], n_fft=n_fft) == 1
    assert analysis.compare_multiple_spectral_roll_off([audio_signal2, audio_signal2],
                                                       [sample_rate2, sample_rate2], n_fft=n_fft) == 1
    assert analysis.compare_multiple_spectral_roll_off([audio_signal3, audio_signal3],
                                                       [sample_rate3, sample_rate3], n_fft=n_fft) == 1
    assert analysis.compare_multiple_spectral_roll_off([audio_signal1, audio_signal2],
                                                       [sample_rate1, sample_rate2], n_fft=n_fft) == 0.8707927973098482
    assert analysis.compare_multiple_spectral_roll_off([audio_signal2, audio_signal1],
                                                       [sample_rate2, sample_rate1], n_fft=n_fft) == 0.8707927973098482
    assert analysis.compare_multiple_spectral_roll_off([audio_signal1, audio_signal3],
                                                       [sample_rate1, sample_rate3], n_fft=n_fft) == 0.8751719403368576
    assert analysis.compare_multiple_spectral_roll_off([audio_signal3, audio_signal1],
                                                       [sample_rate3, sample_rate1], n_fft=n_fft) == 0.8751719403368576
    assert analysis.compare_multiple_spectral_roll_off([audio_signal2, audio_signal3],
                                                       [sample_rate2, sample_rate3], n_fft=n_fft) == 0.994996248365408
    assert analysis.compare_multiple_spectral_roll_off([audio_signal3, audio_signal2],
                                                       [sample_rate3, sample_rate2], n_fft=n_fft) == 0.994996248365408

    assert analysis.compare_multiple_spectral_roll_off([audio_signal1, audio_signal1, audio_signal1],
                                                       [sample_rate1, sample_rate1, sample_rate1], n_fft=n_fft) == 1
    assert analysis.compare_multiple_spectral_roll_off([audio_signal2, audio_signal2, audio_signal2],
                                                       [sample_rate2, sample_rate2, sample_rate2], n_fft=n_fft) == 1
    assert analysis.compare_multiple_spectral_roll_off([audio_signal3, audio_signal3, audio_signal3],
                                                       [sample_rate3, sample_rate3, sample_rate3], n_fft=n_fft) == 1
