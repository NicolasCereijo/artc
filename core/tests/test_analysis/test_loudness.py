import librosa
import pytest
from pathlib import Path

import core.analysis as analysis


@pytest.fixture()
def setup():
    current_path = Path(__file__)

    if current_path.parent.name == 'test_analysis':
        data_path = current_path.parent.parent / 'fixtures'
    elif current_path.parent.name == 'tests':
        data_path = current_path.parent / 'fixtures'
    else:
        data_path = current_path.parent / 'tests' / 'fixtures'

    data_set = {"individual_files":  [
        {"path": data_path, "name": "little-waves.mp3"},
        {"path": data_path, "name": "waves-in-caves.wav"},
        {"path": data_path, "name": "Water Sizzle.mp3"}
    ]}

    return data_set


def test_compare_two_loudness(setup):
    data_set = setup
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] /
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] /
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] /
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_two_loudness(audio_signal1, audio_signal1) == 1
    assert analysis.compare_two_loudness(audio_signal2, audio_signal2) == 1
    assert analysis.compare_two_loudness(audio_signal3, audio_signal3) == 1
    assert round(analysis.compare_two_loudness(audio_signal1, audio_signal2), 5) == 0.88606
    assert round(analysis.compare_two_loudness(audio_signal2, audio_signal1), 5) == 0.88606
    assert round(analysis.compare_two_loudness(audio_signal1, audio_signal3), 5) == 0.73170
    assert round(analysis.compare_two_loudness(audio_signal3, audio_signal1), 5) == 0.73170
    assert round(analysis.compare_two_loudness(audio_signal2, audio_signal3), 5) == 0.73935
    assert round(analysis.compare_two_loudness(audio_signal3, audio_signal2), 5) == 0.73935


def test_compare_multiple_loudness(setup):
    data_set = setup
    audio_signal1, sample_rate1 = librosa.load(data_set["individual_files"][0]["path"] /
                                               data_set["individual_files"][0]["name"])
    audio_signal2, sample_rate2 = librosa.load(data_set["individual_files"][1]["path"] /
                                               data_set["individual_files"][1]["name"])
    audio_signal3, sample_rate3 = librosa.load(data_set["individual_files"][2]["path"] /
                                               data_set["individual_files"][2]["name"])

    assert analysis.compare_multiple_loudness([audio_signal1, audio_signal1]) == 1
    assert analysis.compare_multiple_loudness([audio_signal2, audio_signal2]) == 1
    assert analysis.compare_multiple_loudness([audio_signal3, audio_signal3]) == 1
    assert round(analysis.compare_multiple_loudness([audio_signal1, audio_signal2]), 5) == 0.88606
    assert round(analysis.compare_multiple_loudness([audio_signal2, audio_signal1]), 5) == 0.88606
    assert round(analysis.compare_multiple_loudness([audio_signal1, audio_signal3]), 5) == 0.73170
    assert round(analysis.compare_multiple_loudness([audio_signal3, audio_signal1]), 5) == 0.73170
    assert round(analysis.compare_multiple_loudness([audio_signal2, audio_signal3]), 5) == 0.73935
    assert round(analysis.compare_multiple_loudness([audio_signal3, audio_signal2]), 5) == 0.73935

    assert analysis.compare_multiple_loudness([audio_signal1, audio_signal1, audio_signal1]) == 1
    assert analysis.compare_multiple_loudness([audio_signal2, audio_signal2, audio_signal2]) == 1
    assert analysis.compare_multiple_loudness([audio_signal3, audio_signal3, audio_signal3]) == 1
