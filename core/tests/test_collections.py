import core.artc_collections.harmonize as harm
import core.artc_collections.working_set as w_set
import numpy as np
import pytest


@pytest.fixture()
def setup():
    """
        Selection of the path to the configuration file. When running
        the tests the relative path to the configuration file changes,
        so it is necessary to specify it.

        Returns:
            path (str): Relative path to the configuration file.
            name (str): Name of the configuration file.
            data_set (dict): Audio file paths to test.
    """
    files_path = "../../test_collection/water_sounds/"
    data_set = {"individual_files":  [
        w_set.AudioFile(path=files_path, name="little-waves.mp3",
                        audio_signal_unloaded=lambda: np.zeros(100), sample_rate=44100),
        w_set.AudioFile(path=files_path, name="waves-in-caves.wav",
                        audio_signal_unloaded=lambda: np.zeros(100), sample_rate=44100),
        w_set.AudioFile(path=files_path, name="Water Sizzle.mp3",
                        audio_signal_unloaded=lambda: np.zeros(100), sample_rate=44100)
    ]}

    return "../artc_configurations/", "configurations.json", data_set, files_path


# ----------------------------------------------------------------------------------------------------------------------
# Tests for core.artc_collections.harmonize
# ----------------------------------------------------------------------------------------------------------------------
def test_adjust_length():
    array1 = np.array([0])
    array2 = np.array([1, 2e3])
    array3 = np.array([-1, 2.09, 1e-100])

    assert np.array_equal(harm.adjust_length(array1, array1), (np.array([0], dtype=np.float32),
                                                               np.array([0], dtype=np.float32)))
    assert np.array_equal(harm.adjust_length(array2, array2), (np.array([1, 2e3], dtype=np.float32),
                                                               np.array([1, 2e3], dtype=np.float32)))
    assert np.array_equal(harm.adjust_length(array3, array3), (np.array([-1, 2.09, 1e-100], dtype=np.float32),
                                                               np.array([-1, 2.09, 1e-100], dtype=np.float32)))
    assert np.array_equal(harm.adjust_length(array1, array2), (np.array([0], dtype=np.float32),
                                                               np.array([1], dtype=np.float32)))
    assert np.array_equal(harm.adjust_length(array1, array3), (np.array([0], dtype=np.float32),
                                                               np.array([-1], dtype=np.float32)))
    assert np.array_equal(harm.adjust_length(array2, array3), (np.array([1, 2e3], dtype=np.float32),
                                                               np.array([-1, 2.09], dtype=np.float32)))
    assert np.array_equal(harm.adjust_length(array2, array1), (np.array([1], dtype=np.float32),
                                                               np.array([0], dtype=np.float32)))
    assert np.array_equal(harm.adjust_length(array3, array1), (np.array([-1], dtype=np.float32),
                                                               np.array([0], dtype=np.float32)))
    assert np.array_equal(harm.adjust_length(array3, array2), (np.array([-1, 2.09], dtype=np.float32),
                                                               np.array([1, 2e3], dtype=np.float32)))


def test_normalize_btw_0_1():
    array1 = np.array([0])
    array2 = np.array([0, 2e3])
    array3 = np.array([-1, 2.09, 1e-100])

    compare_1_2 = harm.normalize_btw_0_1(array1, array2)
    compare_1_3 = harm.normalize_btw_0_1(array1, array3)
    compare_2_3 = harm.normalize_btw_0_1(array2, array3)
    compare_3_2 = harm.normalize_btw_0_1(array3, array2)

    assert np.array_equal(compare_1_2[0], np.array([0]))
    assert np.array_equal(compare_1_2[1], np.array([0, 1]))
    assert np.array_equal(compare_1_3[0], np.array([0.3236245954692557]))
    assert np.array_equal(compare_1_3[1], np.array([0, 1, 0.3236245954692557]))
    assert np.array_equal(compare_2_3[0], np.array([0.0004997501249375312, 1]))
    assert np.array_equal(compare_2_3[1], np.array([0, 0.0015442278860569715, 0.0004997501249375312]))
    assert np.array_equal(compare_3_2[0], np.array([0, 0.0015442278860569715, 0.0004997501249375312]))
    assert np.array_equal(compare_3_2[1], np.array([0.0004997501249375312, 1]))


# ----------------------------------------------------------------------------------------------------------------------
# Tests for core.artc_collections.working_set
# ----------------------------------------------------------------------------------------------------------------------
def test_search_file(setup):
    path, name, data_set, _ = setup
    test_set = w_set.WorkingSet("test_set", True, data_set)

    assert test_set.__contains__(data_set["individual_files"][0].name, "individual_files")
    assert test_set.__contains__(data_set["individual_files"][1].name, "individual_files")
    assert test_set.__contains__(data_set["individual_files"][2].name, "individual_files")

    assert test_set.__contains__("", "") is False
    assert test_set.__contains__(data_set["individual_files"][2].name, "") is False
    assert test_set.__contains__("", "individual_files") is False
    assert test_set.__contains__(data_set["individual_files"][2].name, "invalid_group") is False
    assert test_set.__contains__("invalid_file", "individual_files") is False


def test_add_file(setup):
    path, name, data_set, files_path = setup
    test_set = w_set.WorkingSet("test_set", True, data_set)

    assert test_set.add_file(files_path, "smallwaves1.mp3", path + name)

    assert test_set.add_file("", "", "") is False
    assert test_set.add_file("", "smallwaves1.mp3", path + name) is False
    assert test_set.add_file(files_path, "smallwaves1.mp3", "") is False
    assert test_set.add_file(files_path, "", path + name) is False
    assert test_set.add_file("invalid_path", "smallwaves1.mp3", path + name) is False
    assert test_set.add_file(files_path, "smallwaves1.mp3", "invalid_config_path") is False
    assert test_set.add_file(files_path, "invalid_name", path + name) is False


def test_remove_file(setup):
    path, name, data_set, _ = setup
    test_set = w_set.WorkingSet("test_set", True, data_set)

    assert test_set.remove_file("little-waves.mp3")
    assert test_set.remove_file(data_set["individual_files"][1].name, "individual_files")

    assert test_set.remove_file("", "") is False
    assert test_set.remove_file("", "individual_files") is False
    assert test_set.remove_file(data_set["individual_files"][0].name, "") is False
    assert test_set.remove_file("invalid_name", "individual_files") is False
    assert test_set.remove_file(data_set["individual_files"][0].name, "invalid_group") is False


def test_add_directory(setup):
    path, name, data_set, _ = setup
    test_set = w_set.WorkingSet("test_set", True, data_set)

    assert test_set.add_directory("../../test_collection/water_sounds/", path + name, "individual_files")
    assert test_set.add_directory("../../test_collection/water_sounds/", path + name, "new_group")

    assert test_set.add_directory("", "", "") is False
    assert test_set.add_directory("", path + name, "individual_files") is False
    assert test_set.add_directory("../../test_collection/water_sounds/", "", "individual_files") is False
    assert test_set.add_directory("../../test_collection/water_sounds/", path + name, "") is False
    assert test_set.add_directory("invalid_path", path + name, "individual_files") is False
    assert test_set.add_directory("../../test_collection/water_sounds/", "invalid_config_path",
                                  "individual_files") is False
