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


def test_compare_two_zcr(setup):
    data_set = setup
    audio_signal1, sample_rate1 = load(data_set["individual_files"][0]["path"] /
                                       data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = load(data_set["individual_files"][1]["path"] /
                                       data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = load(data_set["individual_files"][2]["path"] /
                                       data_set["individual_files"][2]["name"])

    assert analysis.compare_two_zcr(audio_signal1, audio_signal1) == 1
    assert analysis.compare_two_zcr(audio_signal2, audio_signal2) == 1
    assert analysis.compare_two_zcr(audio_signal3, audio_signal3) == 1
    assert round(analysis.compare_two_zcr(audio_signal1, audio_signal2), 5) == 0.3398
    assert round(analysis.compare_two_zcr(audio_signal2, audio_signal1), 5) == 0.3398
    assert round(analysis.compare_two_zcr(audio_signal1, audio_signal3), 5) == 0.35384
    assert round(analysis.compare_two_zcr(audio_signal3, audio_signal1), 5) == 0.35384
    assert round(analysis.compare_two_zcr(audio_signal2, audio_signal3), 5) == 0.83234
    assert round(analysis.compare_two_zcr(audio_signal3, audio_signal2), 5) == 0.83234


def test_compare_multiple_zcr(setup):
    data_set = setup
    audio_signal1, sample_rate1 = load(data_set["individual_files"][0]["path"] /
                                       data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = load(data_set["individual_files"][1]["path"] /
                                       data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = load(data_set["individual_files"][2]["path"] /
                                       data_set["individual_files"][2]["name"])

    assert analysis.compare_multiple_zcr([audio_signal1, audio_signal1]) == 1
    assert analysis.compare_multiple_zcr([audio_signal2, audio_signal2]) == 1
    assert analysis.compare_multiple_zcr([audio_signal3, audio_signal3]) == 1
    assert round(analysis.compare_multiple_zcr([audio_signal1, audio_signal2]), 5) == 0.3398
    assert round(analysis.compare_multiple_zcr([audio_signal2, audio_signal1]), 5) == 0.3398
    assert round(analysis.compare_multiple_zcr([audio_signal1, audio_signal3]), 5) == 0.35384
    assert round(analysis.compare_multiple_zcr([audio_signal3, audio_signal1]), 5) == 0.35384
    assert round(analysis.compare_multiple_zcr([audio_signal2, audio_signal3]), 5) == 0.83234
    assert round(analysis.compare_multiple_zcr([audio_signal3, audio_signal2]), 5) == 0.83234

    assert analysis.compare_multiple_zcr([audio_signal1, audio_signal1, audio_signal1]) == 1
    assert analysis.compare_multiple_zcr([audio_signal2, audio_signal2, audio_signal2]) == 1
    assert analysis.compare_multiple_zcr([audio_signal3, audio_signal3, audio_signal3]) == 1
