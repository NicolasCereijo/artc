import core.datastructures as dt_structs
import importlib.resources
import numpy as np
import pytest


@pytest.fixture()
def setup():
    configuration_path = str(importlib.resources.files('core.configurations') / 'default_configurations.json')
    files_path = str(importlib.resources.path('test_collection.water_sounds', '')) + '/'

    data_set = {"individual_files":  [
        dt_structs.AudioFile(path=files_path, name="little-waves.mp3",
                             audio_signal_unloaded=lambda: np.zeros(100), sample_rate=44100),
        dt_structs.AudioFile(path=files_path, name="waves-in-caves.wav",
                             audio_signal_unloaded=lambda: np.zeros(100), sample_rate=44100),
        dt_structs.AudioFile(path=files_path, name="Water Sizzle.mp3",
                             audio_signal_unloaded=lambda: np.zeros(100), sample_rate=44100)
    ]}

    return configuration_path, files_path, data_set


# ----------------------------------------------------------------------------------------------------------------------
# Tests for core.datastructures.harmonize
# ----------------------------------------------------------------------------------------------------------------------
def test_adjust_length():
    array1 = np.array([0])
    array2 = np.array([1, 2e3])
    array3 = np.array([-1, 2.09, 1e-100])

    assert np.array_equal(dt_structs.adjust_length(array1, array1), (np.array([0], dtype=np.float32),
                                                                     np.array([0], dtype=np.float32)))
    assert np.array_equal(dt_structs.adjust_length(array2, array2), (np.array([1, 2e3], dtype=np.float32),
                                                                     np.array([1, 2e3], dtype=np.float32)))
    assert np.array_equal(dt_structs.adjust_length(array3, array3), (np.array([-1, 2.09, 1e-100], dtype=np.float32),
                                                                     np.array([-1, 2.09, 1e-100], dtype=np.float32)))
    assert np.array_equal(dt_structs.adjust_length(array1, array2), (np.array([0], dtype=np.float32),
                                                                     np.array([1], dtype=np.float32)))
    assert np.array_equal(dt_structs.adjust_length(array1, array3), (np.array([0], dtype=np.float32),
                                                                     np.array([-1], dtype=np.float32)))
    assert np.array_equal(dt_structs.adjust_length(array2, array3), (np.array([1, 2e3], dtype=np.float32),
                                                                     np.array([-1, 2.09], dtype=np.float32)))
    assert np.array_equal(dt_structs.adjust_length(array2, array1), (np.array([1], dtype=np.float32),
                                                                     np.array([0], dtype=np.float32)))
    assert np.array_equal(dt_structs.adjust_length(array3, array1), (np.array([-1], dtype=np.float32),
                                                                     np.array([0], dtype=np.float32)))
    assert np.array_equal(dt_structs.adjust_length(array3, array2), (np.array([-1, 2.09], dtype=np.float32),
                                                                     np.array([1, 2e3], dtype=np.float32)))


def test_normalize_btw_0_1():
    array1 = np.array([0])
    array2 = np.array([0, 2e3])
    array3 = np.array([-1, 2.09, 1e-100])

    compare_1_2 = dt_structs.normalize_btw_0_1(array1, array2)
    compare_1_3 = dt_structs.normalize_btw_0_1(array1, array3)
    compare_2_3 = dt_structs.normalize_btw_0_1(array2, array3)
    compare_3_2 = dt_structs.normalize_btw_0_1(array3, array2)

    assert np.array_equal(compare_1_2[0], np.array([0]))
    assert np.array_equal(compare_1_2[1], np.array([0, 1]))
    assert np.array_equal(compare_1_3[0], np.array([0.3236245954692557]))
    assert np.array_equal(compare_1_3[1], np.array([0, 1, 0.3236245954692557]))
    assert np.array_equal(compare_2_3[0], np.array([0.0004997501249375312, 1]))
    assert np.array_equal(compare_2_3[1], np.array([0, 0.0015442278860569715, 0.0004997501249375312]))
    assert np.array_equal(compare_3_2[0], np.array([0, 0.0015442278860569715, 0.0004997501249375312]))
    assert np.array_equal(compare_3_2[1], np.array([0.0004997501249375312, 1]))


# ----------------------------------------------------------------------------------------------------------------------
# Tests for core.datastructures.working_set
# ----------------------------------------------------------------------------------------------------------------------
def test_search_file(setup):
    _, _, data_set = setup
    test_set = dt_structs.WorkingSet("test_set", True, data_set)

    assert test_set.__contains__(data_set["individual_files"][0].name, "individual_files")
    assert test_set.__contains__(data_set["individual_files"][1].name, "individual_files")
    assert test_set.__contains__(data_set["individual_files"][2].name, "individual_files")

    assert test_set.__contains__("", "") is False
    assert test_set.__contains__(data_set["individual_files"][2].name, "") is False
    assert test_set.__contains__("", "individual_files") is False
    assert test_set.__contains__(data_set["individual_files"][2].name, "invalid_group") is False
    assert test_set.__contains__("invalid_file", "individual_files") is False


def test_add_file(setup):
    configuration_path, files_path, data_set = setup
    test_set = dt_structs.WorkingSet("test_set", True, data_set)

    assert test_set.add_file(files_path, "smallwaves1.mp3", configuration_path)

    assert test_set.add_file("", "", "") is False
    assert test_set.add_file("", "smallwaves1.mp3", configuration_path) is False
    assert test_set.add_file(files_path, "smallwaves1.mp3", "") is False
    assert test_set.add_file(files_path, "", configuration_path) is False
    assert test_set.add_file("invalid_path", "smallwaves1.mp3", configuration_path) is False
    assert test_set.add_file(files_path, "smallwaves1.mp3", "invalid_config_path") is False
    assert test_set.add_file(files_path, "invalid_name", configuration_path) is False


def test_remove_file(setup):
    _, _, data_set = setup
    test_set = dt_structs.WorkingSet("test_set", True, data_set)

    assert test_set.remove_file("little-waves.mp3")
    assert test_set.remove_file(data_set["individual_files"][1].name, "individual_files")

    assert test_set.remove_file("", "") is False
    assert test_set.remove_file("", "individual_files") is False
    assert test_set.remove_file(data_set["individual_files"][0].name, "") is False
    assert test_set.remove_file("invalid_name", "individual_files") is False
    assert test_set.remove_file(data_set["individual_files"][0].name, "invalid_group") is False


def test_add_directory(setup):
    configuration_path, files_path, data_set = setup
    test_set = dt_structs.WorkingSet("test_set", True, data_set)

    assert test_set.add_directory(files_path, configuration_path, "individual_files")
    assert test_set.add_directory(files_path, configuration_path, "new_group")

    assert test_set.add_directory("", "", "") is False
    assert test_set.add_directory("", configuration_path, "individual_files") is False
    assert test_set.add_directory(files_path, "", "individual_files") is False
    assert test_set.add_directory(files_path, configuration_path, "") is False
    assert test_set.add_directory("invalid_path", configuration_path, "individual_files") is False
    assert test_set.add_directory(files_path, "invalid_config_path", "individual_files") is False
