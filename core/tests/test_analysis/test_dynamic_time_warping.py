from pathlib import Path

import pytest
from librosa import load

import core.analysis as analysis


@pytest.fixture()
def setup():
    execution_path = Path(__file__)

    base_path = execution_path.parent
    fixtures_path = {
        'test_analysis': base_path.parent / 'fixtures',     # Path when running from 'test_analysis'
        'tests': base_path / 'fixtures',                    # Path when running from 'tests'
    }.get(base_path.name, base_path / 'tests' / 'fixtures') # Default, when running from 'core'

    data_set = {"individual_files":  [
        {"path": fixtures_path, "name": "little-waves.mp3"},
        {"path": fixtures_path, "name": "waves-in-caves.wav"},
        {"path": fixtures_path, "name": "Water Sizzle.mp3"}
    ]}

    return data_set


def test_compare_two_dtw(setup):
    data_set = setup
    n_fft = 512
    audio_signal1, sample_rate1 = load(data_set["individual_files"][0]["path"] /
                                       data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = load(data_set["individual_files"][1]["path"] /
                                       data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = load(data_set["individual_files"][2]["path"] /
                                       data_set["individual_files"][2]["name"])

    assert analysis.compare_two_dtw(audio_signal1, audio_signal1, sample_rate1, sample_rate1,
                                    n_fft=n_fft) == 1
    assert analysis.compare_two_dtw(audio_signal2, audio_signal2, sample_rate2, sample_rate2,
                                    n_fft=n_fft) == 1
    assert analysis.compare_two_dtw(audio_signal3, audio_signal3, sample_rate3, sample_rate3,
                                    n_fft=n_fft) == 1
    assert round(analysis.compare_two_dtw(audio_signal1, audio_signal2, sample_rate1, sample_rate2,
                                          n_fft=n_fft), 5) == 0.0
    assert round(analysis.compare_two_dtw(audio_signal2, audio_signal1, sample_rate2, sample_rate1,
                                          n_fft=n_fft), 5) == 0.0
    assert round(analysis.compare_two_dtw(audio_signal1, audio_signal3, sample_rate1, sample_rate3,
                                          n_fft=n_fft), 5) == 0.17461
    assert round(analysis.compare_two_dtw(audio_signal3, audio_signal1, sample_rate3, sample_rate1,
                                          n_fft=n_fft), 5) == 0.17461
    assert round(analysis.compare_two_dtw(audio_signal2, audio_signal3, sample_rate2, sample_rate3,
                                          n_fft=n_fft), 5) == 0.05946
    assert round(analysis.compare_two_dtw(audio_signal3, audio_signal2, sample_rate3, sample_rate2,
                                          n_fft=n_fft), 5) == 0.05946


def test_compare_multiple_dtw(setup):
    data_set = setup
    n_fft = 512
    audio_signal1, sample_rate1 = load(data_set["individual_files"][0]["path"] /
                                       data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = load(data_set["individual_files"][1]["path"] /
                                       data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = load(data_set["individual_files"][2]["path"] /
                                       data_set["individual_files"][2]["name"])

    assert analysis.compare_multiple_dtw([audio_signal1, audio_signal1],
                                         [sample_rate1, sample_rate1],
                                         n_fft=n_fft) == 1
    assert analysis.compare_multiple_dtw([audio_signal2, audio_signal2],
                                         [sample_rate2, sample_rate2],
                                         n_fft=n_fft) == 1
    assert analysis.compare_multiple_dtw([audio_signal3, audio_signal3],
                                         [sample_rate3, sample_rate3],
                                         n_fft=n_fft) == 1
    assert round(analysis.compare_multiple_dtw([audio_signal1, audio_signal2],
                                               [sample_rate1, sample_rate2],
                                               n_fft=n_fft), 5) == 0.0
    assert round(analysis.compare_multiple_dtw([audio_signal2, audio_signal1],
                                               [sample_rate2, sample_rate1],
                                               n_fft=n_fft), 5) == 0.0
    assert round(analysis.compare_multiple_dtw([audio_signal1, audio_signal3],
                                               [sample_rate1, sample_rate3],
                                               n_fft=n_fft), 5) == 0.17461
    assert round(analysis.compare_multiple_dtw([audio_signal3, audio_signal1],
                                               [sample_rate3, sample_rate1],
                                               n_fft=n_fft), 5) == 0.17461
    assert round(analysis.compare_multiple_dtw([audio_signal2, audio_signal3],
                                               [sample_rate2, sample_rate3],
                                               n_fft=n_fft), 5) == 0.05946
    assert round(analysis.compare_multiple_dtw([audio_signal3, audio_signal2],
                                               [sample_rate3, sample_rate2],
                                               n_fft=n_fft), 5) == 0.05946

    assert analysis.compare_multiple_dtw([audio_signal1, audio_signal1, audio_signal1],
                                         [sample_rate1, sample_rate1, sample_rate1],
                                         n_fft=n_fft) == 1
    assert analysis.compare_multiple_dtw([audio_signal2, audio_signal2, audio_signal2],
                                         [sample_rate2, sample_rate2, sample_rate2],
                                         n_fft=n_fft) == 1
    assert analysis.compare_multiple_dtw([audio_signal3, audio_signal3, audio_signal3],
                                         [sample_rate3, sample_rate3, sample_rate3],
                                         n_fft=n_fft) == 1
