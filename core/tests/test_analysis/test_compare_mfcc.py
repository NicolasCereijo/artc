import core.artc_analysis as analysis
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


def test_compare_two_mfcc(setup):
    data_set = setup
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] +
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] +
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] +
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_two_mfcc(audio_signal1, audio_signal1, sample_rate1, sample_rate1) == 1
    assert analysis.compare_two_mfcc(audio_signal2, audio_signal2, sample_rate2, sample_rate2) == 1
    assert analysis.compare_two_mfcc(audio_signal3, audio_signal3, sample_rate3, sample_rate3) == 1
    assert analysis.compare_two_mfcc(audio_signal1, audio_signal2, sample_rate1, sample_rate2) == 0.8113852739334106
    assert analysis.compare_two_mfcc(audio_signal2, audio_signal1, sample_rate2, sample_rate1) == 0.8113852739334106
    assert analysis.compare_two_mfcc(audio_signal1, audio_signal3, sample_rate1, sample_rate3) == 0.85392165184021
    assert analysis.compare_two_mfcc(audio_signal3, audio_signal1, sample_rate3, sample_rate1) == 0.85392165184021
    assert analysis.compare_two_mfcc(audio_signal2, audio_signal3, sample_rate2, sample_rate3) == 0.7408664226531982
    assert analysis.compare_two_mfcc(audio_signal3, audio_signal2, sample_rate3, sample_rate2) == 0.7408664226531982
