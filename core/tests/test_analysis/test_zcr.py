import core.analysis as analysis
import numpy as np
import librosa
import pytest


@pytest.fixture()
def setup():
    """
        Audio files for testing. When running the tests the relative
        path to the files changes, so it is necessary to specify it.

        Returns:
            data_set (dict): Dictionary with file paths.
    """
    files_path = "../../test_collection/water_sounds/"
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
    assert analysis.compare_two_zcr(audio_signal1, audio_signal2) == 0.4703782140435168
    assert analysis.compare_two_zcr(audio_signal2, audio_signal1) == 0.4703782140435168
    assert analysis.compare_two_zcr(audio_signal1, audio_signal3) == 0.3154215272606933
    assert analysis.compare_two_zcr(audio_signal3, audio_signal1) == 0.3154215272606933
    assert analysis.compare_two_zcr(audio_signal2, audio_signal3) == 0.44035933417840545
    assert analysis.compare_two_zcr(audio_signal3, audio_signal2) == 0.44035933417840545


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
    assert analysis.compare_multiple_zcr([audio_signal1, audio_signal2]) == 0.4703782140435168
    assert analysis.compare_multiple_zcr([audio_signal2, audio_signal1]) == 0.4703782140435168
    assert analysis.compare_multiple_zcr([audio_signal1, audio_signal3]) == 0.3154215272606933
    assert analysis.compare_multiple_zcr([audio_signal3, audio_signal1]) == 0.3154215272606933
    assert analysis.compare_multiple_zcr([audio_signal2, audio_signal3]) == 0.44035933417840545
    assert analysis.compare_multiple_zcr([audio_signal3, audio_signal2]) == 0.44035933417840545

    assert analysis.compare_multiple_zcr([audio_signal1, audio_signal1, audio_signal1]) == 1
    assert analysis.compare_multiple_zcr([audio_signal2, audio_signal2, audio_signal2]) == 1
    assert analysis.compare_multiple_zcr([audio_signal3, audio_signal3, audio_signal3]) == 1
