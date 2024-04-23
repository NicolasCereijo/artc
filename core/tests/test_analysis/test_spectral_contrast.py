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


def test_compare_two_sp_contrast(setup):
    data_set = setup
    hop_length = 2048
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] +
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] +
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] +
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_two_spectral_contrast(audio_signal1, audio_signal1,
                                                  sample_rate1, sample_rate1, hop_length) == 1
    assert analysis.compare_two_spectral_contrast(audio_signal2, audio_signal2,
                                                  sample_rate2, sample_rate2, hop_length) == 1
    assert analysis.compare_two_spectral_contrast(audio_signal3, audio_signal3,
                                                  sample_rate3, sample_rate3, hop_length) == 1
    assert analysis.compare_two_spectral_contrast(audio_signal1, audio_signal2,
                                                  sample_rate1, sample_rate2, hop_length) == 0.9595097341913768
    assert analysis.compare_two_spectral_contrast(audio_signal2, audio_signal1,
                                                  sample_rate2, sample_rate1, hop_length) == 0.9595097341913768
    assert analysis.compare_two_spectral_contrast(audio_signal1, audio_signal3,
                                                  sample_rate1, sample_rate3, hop_length) == 0.9645128780338763
    assert analysis.compare_two_spectral_contrast(audio_signal3, audio_signal1,
                                                  sample_rate3, sample_rate1, hop_length) == 0.9645128780338763
    assert analysis.compare_two_spectral_contrast(audio_signal2, audio_signal3,
                                                  sample_rate2, sample_rate3, hop_length) == 0.9746462489641077
    assert analysis.compare_two_spectral_contrast(audio_signal3, audio_signal2,
                                                  sample_rate3, sample_rate2, hop_length) == 0.9746462489641077


def test_compare_multiple_sp_contrast(setup):
    data_set = setup
    hop_length = 2048
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] +
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] +
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] +
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_multiple_spectral_contrast([audio_signal1, audio_signal1],
                                                       [sample_rate1, sample_rate1], hop_length) == 1
    assert analysis.compare_multiple_spectral_contrast([audio_signal2, audio_signal2],
                                                       [sample_rate2, sample_rate2], hop_length) == 1
    assert analysis.compare_multiple_spectral_contrast([audio_signal3, audio_signal3],
                                                       [sample_rate3, sample_rate3], hop_length) == 1
    assert analysis.compare_multiple_spectral_contrast([audio_signal1, audio_signal2],
                                                       [sample_rate1, sample_rate2], hop_length) == 0.9595097341913768
    assert analysis.compare_multiple_spectral_contrast([audio_signal2, audio_signal1],
                                                       [sample_rate2, sample_rate1], hop_length) == 0.9595097341913768
    assert analysis.compare_multiple_spectral_contrast([audio_signal1, audio_signal3],
                                                       [sample_rate1, sample_rate3], hop_length) == 0.9645128780338763
    assert analysis.compare_multiple_spectral_contrast([audio_signal3, audio_signal1],
                                                       [sample_rate3, sample_rate1], hop_length) == 0.9645128780338763
    assert analysis.compare_multiple_spectral_contrast([audio_signal2, audio_signal3],
                                                       [sample_rate2, sample_rate3], hop_length) == 0.9746462489641077
    assert analysis.compare_multiple_spectral_contrast([audio_signal3, audio_signal2],
                                                       [sample_rate3, sample_rate2], hop_length) == 0.9746462489641077

    assert analysis.compare_multiple_spectral_contrast([audio_signal1, audio_signal1, audio_signal1],
                                                       [sample_rate1, sample_rate1, sample_rate1], hop_length) == 1
    assert analysis.compare_multiple_spectral_contrast([audio_signal2, audio_signal2, audio_signal2],
                                                       [sample_rate2, sample_rate2, sample_rate2], hop_length) == 1
    assert analysis.compare_multiple_spectral_contrast([audio_signal3, audio_signal3, audio_signal3],
                                                       [sample_rate3, sample_rate3, sample_rate3], hop_length) == 1