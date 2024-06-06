import core.analysis as analysis
import importlib.resources
import numpy as np
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


def test_check_zcr():
    array1 = np.array([])
    array2 = np.array([1])
    array3 = np.array([-1])
    array4 = np.array([1, -2e3])
    array5 = np.array([-1, 2e3])
    array6 = np.array([-1, 2.09, -98])

    assert analysis.check_zcr(array1) == (False, 0)
    assert analysis.check_zcr(array2) == (True, 1)
    assert analysis.check_zcr(array3) == (True, 1)
    assert analysis.check_zcr(array4) == (True, 2)
    assert analysis.check_zcr(array5) == (True, 2)
    assert analysis.check_zcr(array6) == (True, 3)


def test_compare_two_zcr(setup):
    data_set = setup
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] +
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] +
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] +
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_two_zcr(audio_signal1, audio_signal1) == 1
    assert analysis.compare_two_zcr(audio_signal2, audio_signal2) == 1
    assert analysis.compare_two_zcr(audio_signal3, audio_signal3) == 1
    assert analysis.compare_two_zcr(audio_signal1, audio_signal2) == 0.4700966477394104
    assert analysis.compare_two_zcr(audio_signal2, audio_signal1) == 0.4700966477394104
    assert analysis.compare_two_zcr(audio_signal1, audio_signal3) == 0.31544044613838196
    assert analysis.compare_two_zcr(audio_signal3, audio_signal1) == 0.31544044613838196
    assert analysis.compare_two_zcr(audio_signal2, audio_signal3) == 0.4404390752315521
    assert analysis.compare_two_zcr(audio_signal3, audio_signal2) == 0.4404390752315521


def test_compare_multiple_zcr(setup):
    data_set = setup
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] +
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] +
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] +
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_multiple_zcr([audio_signal1, audio_signal1]) == 1
    assert analysis.compare_multiple_zcr([audio_signal2, audio_signal2]) == 1
    assert analysis.compare_multiple_zcr([audio_signal3, audio_signal3]) == 1
    assert analysis.compare_multiple_zcr([audio_signal1, audio_signal2]) == 0.4700966477394104
    assert analysis.compare_multiple_zcr([audio_signal2, audio_signal1]) == 0.4700966477394104
    assert analysis.compare_multiple_zcr([audio_signal1, audio_signal3]) == 0.31544044613838196
    assert analysis.compare_multiple_zcr([audio_signal3, audio_signal1]) == 0.31544044613838196
    assert analysis.compare_multiple_zcr([audio_signal2, audio_signal3]) == 0.4404390752315521
    assert analysis.compare_multiple_zcr([audio_signal3, audio_signal2]) == 0.4404390752315521

    assert analysis.compare_multiple_zcr([audio_signal1, audio_signal1, audio_signal1]) == 1
    assert analysis.compare_multiple_zcr([audio_signal2, audio_signal2, audio_signal2]) == 1
    assert analysis.compare_multiple_zcr([audio_signal3, audio_signal3, audio_signal3]) == 1
