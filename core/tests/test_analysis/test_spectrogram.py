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


def test_compare_two_spectrograms(setup):
    data_set = setup
    n_fft = 2048
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] +
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] +
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] +
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_two_spectrograms(audio_signal1, audio_signal1, n_fft) == 1
    assert analysis.compare_two_spectrograms(audio_signal2, audio_signal2, n_fft) == 1
    assert analysis.compare_two_spectrograms(audio_signal3, audio_signal3, n_fft) == 1
    assert analysis.compare_two_spectrograms(audio_signal1, audio_signal2, n_fft) == 0.23510941863059998
    assert analysis.compare_two_spectrograms(audio_signal2, audio_signal1, n_fft) == 0.23510941863059998
    assert analysis.compare_two_spectrograms(audio_signal1, audio_signal3, n_fft) == 0.03373456746339798
    assert analysis.compare_two_spectrograms(audio_signal3, audio_signal1, n_fft) == 0.03373456746339798
    assert analysis.compare_two_spectrograms(audio_signal2, audio_signal3, n_fft) == 0.16679933667182922
    assert analysis.compare_two_spectrograms(audio_signal3, audio_signal2, n_fft) == 0.16679933667182922


def test_compare_multiple_spectrograms(setup):
    data_set = setup
    n_fft = 2048
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] +
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] +
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] +
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_multiple_spectrograms([audio_signal1, audio_signal1], n_fft) == 1
    assert analysis.compare_multiple_spectrograms([audio_signal2, audio_signal2], n_fft) == 1
    assert analysis.compare_multiple_spectrograms([audio_signal3, audio_signal3], n_fft) == 1
    assert analysis.compare_multiple_spectrograms([audio_signal1, audio_signal2], n_fft) == 0.23510941863059998
    assert analysis.compare_multiple_spectrograms([audio_signal2, audio_signal1], n_fft) == 0.23510941863059998
    assert analysis.compare_multiple_spectrograms([audio_signal1, audio_signal3], n_fft) == 0.03373456746339798
    assert analysis.compare_multiple_spectrograms([audio_signal3, audio_signal1], n_fft) == 0.03373456746339798
    assert analysis.compare_multiple_spectrograms([audio_signal2, audio_signal3], n_fft) == 0.16679933667182922
    assert analysis.compare_multiple_spectrograms([audio_signal3, audio_signal2], n_fft) == 0.16679933667182922

    assert analysis.compare_multiple_spectrograms([audio_signal1, audio_signal1, audio_signal1], n_fft) == 1
    assert analysis.compare_multiple_spectrograms([audio_signal2, audio_signal2, audio_signal2], n_fft) == 1
    assert analysis.compare_multiple_spectrograms([audio_signal3, audio_signal3, audio_signal3], n_fft) == 1
