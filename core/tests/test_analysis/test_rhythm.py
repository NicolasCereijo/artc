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


def test_compare_two_rhythm(setup):
    data_set = setup
    hop_length = 1024
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] +
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] +
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] +
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_two_rhythm(audio_signal1, audio_signal1,
                                       sample_rate1, sample_rate1, hop_length=hop_length) == 1
    assert analysis.compare_two_rhythm(audio_signal2, audio_signal2,
                                       sample_rate2, sample_rate2, hop_length=hop_length) == 1
    assert analysis.compare_two_rhythm(audio_signal3, audio_signal3,
                                       sample_rate3, sample_rate3, hop_length=hop_length) == 1
    assert analysis.compare_two_rhythm(audio_signal1, audio_signal2,
                                       sample_rate1, sample_rate2, hop_length=hop_length) == 0.8333333333333334
    assert analysis.compare_two_rhythm(audio_signal2, audio_signal1,
                                       sample_rate2, sample_rate1, hop_length=hop_length) == 0.8333333333333334
    assert analysis.compare_two_rhythm(audio_signal1, audio_signal3,
                                       sample_rate1, sample_rate3, hop_length=hop_length) == 0.9
    assert analysis.compare_two_rhythm(audio_signal3, audio_signal1,
                                       sample_rate3, sample_rate1, hop_length=hop_length) == 0.9
    assert analysis.compare_two_rhythm(audio_signal2, audio_signal3,
                                       sample_rate2, sample_rate3, hop_length=hop_length) == 0.75
    assert analysis.compare_two_rhythm(audio_signal3, audio_signal2,
                                       sample_rate3, sample_rate2, hop_length=hop_length) == 0.75


def test_compare_multiple_rhythm(setup):
    data_set = setup
    hop_length = 1024
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] +
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] +
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] +
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_multiple_rhythm([audio_signal1, audio_signal1],
                                            [sample_rate1, sample_rate1], hop_length=hop_length) == 1
    assert analysis.compare_multiple_rhythm([audio_signal2, audio_signal2],
                                            [sample_rate2, sample_rate2], hop_length=hop_length) == 1
    assert analysis.compare_multiple_rhythm([audio_signal3, audio_signal3],
                                            [sample_rate3, sample_rate3], hop_length=hop_length) == 1
    assert analysis.compare_multiple_rhythm([audio_signal1, audio_signal2],
                                            [sample_rate1, sample_rate2], hop_length=hop_length) == 0.8333333333333334
    assert analysis.compare_multiple_rhythm([audio_signal2, audio_signal1],
                                            [sample_rate2, sample_rate1], hop_length=hop_length) == 0.8333333333333334
    assert analysis.compare_multiple_rhythm([audio_signal1, audio_signal3],
                                            [sample_rate1, sample_rate3], hop_length=hop_length) == 0.9
    assert analysis.compare_multiple_rhythm([audio_signal3, audio_signal1],
                                            [sample_rate3, sample_rate1], hop_length=hop_length) == 0.9
    assert analysis.compare_multiple_rhythm([audio_signal2, audio_signal3],
                                            [sample_rate2, sample_rate3], hop_length=hop_length) == 0.75
    assert analysis.compare_multiple_rhythm([audio_signal3, audio_signal2],
                                            [sample_rate3, sample_rate2], hop_length=hop_length) == 0.75

    assert analysis.compare_multiple_rhythm([audio_signal1, audio_signal1, audio_signal1],
                                            [sample_rate1, sample_rate1, sample_rate1], hop_length=hop_length) == 1
    assert analysis.compare_multiple_rhythm([audio_signal2, audio_signal2, audio_signal2],
                                            [sample_rate2, sample_rate2, sample_rate2], hop_length=hop_length) == 1
    assert analysis.compare_multiple_rhythm([audio_signal3, audio_signal3, audio_signal3],
                                            [sample_rate3, sample_rate3, sample_rate3], hop_length=hop_length) == 1
