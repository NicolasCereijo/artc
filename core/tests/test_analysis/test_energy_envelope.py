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

    assert analysis.compare_two_energy_envelope(audio_signal1, audio_signal1) == 1
    assert analysis.compare_two_energy_envelope(audio_signal2, audio_signal2) == 1
    assert analysis.compare_two_energy_envelope(audio_signal3, audio_signal3) == 1
    assert analysis.compare_two_energy_envelope(audio_signal1, audio_signal2) == 0.459095561268075
    assert analysis.compare_two_energy_envelope(audio_signal2, audio_signal1) == 0.459095561268075
    assert analysis.compare_two_energy_envelope(audio_signal1, audio_signal3) == 0.4848934342383823
    assert analysis.compare_two_energy_envelope(audio_signal3, audio_signal1) == 0.4848934342383823
    assert analysis.compare_two_energy_envelope(audio_signal2, audio_signal3) == 0.5837413097561219
    assert analysis.compare_two_energy_envelope(audio_signal3, audio_signal2) == 0.5837413097561219
