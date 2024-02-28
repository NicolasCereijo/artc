import core.artc_collections.working_set as w_set
import pytest


@pytest.fixture()
def setup():
    """
        Selection of the path to the configuration file. When running
        the tests the relative path to the configuration file changes,
        so it is necessary to specify it.

        Returns:
            path: Relative path to the configuration file.
            name: Name of the configuration file.
    """
    files_path = "../../test_collection/water_sounds/"
    data_set = {"individual_files":  [
        {"path": files_path, "name": "little-waves.mp3"},
        {"path": files_path, "name": "waves-in-caves.wav"},
        {"path": files_path, "name": "Water Sizzle.mp3"}
    ]}

    return "../artc_configurations/", "configurations.json", data_set


def test_search_file(setup):
    path, name, data_set = setup
    test_set = w_set.WorkingSet(True, data_set)

    assert test_set.search_file("little-waves.mp3", "individual_files")
    assert test_set.search_file("waves-in-caves.wav", "individual_files")
    assert test_set.search_file("Water Sizzle.mp3", "individual_files")

    assert test_set.search_file("", "") is False
    assert test_set.search_file("Water Sizzle.mp3", "") is False
    assert test_set.search_file("", "individual_files") is False
    assert test_set.search_file("Water Sizzle.mp3", "invalid_group") is False
    assert test_set.search_file("invalid_file", "individual_files") is False


def test_add_file(setup):
    path, name, data_set = setup
    test_set = w_set.WorkingSet(True, data_set)

    assert test_set.add_file("../../test_collection/water_sounds/", "smallwaves1.mp3", path + name)

    assert test_set.add_file("", "", "") is False
    assert test_set.add_file("", "smallwaves1.mp3", path + name) is False
    assert test_set.add_file("../../test_collection/water_sounds/", "smallwaves1.mp3",
                             "") is False
    assert test_set.add_file("../../test_collection/water_sounds/", "", path + name) is False
    assert test_set.add_file("invalid_path", "smallwaves1.mp3", path + name) is False
    assert test_set.add_file("../../test_collection/water_sounds/", "smallwaves1.mp3",
                             "invalid_config_path") is False
    assert test_set.add_file("../../test_collection/water_sounds/", "invalid_name", path + name) is False


def test_remove_file(setup):
    path, name, data_set = setup
    test_set = w_set.WorkingSet(True, data_set)

    assert test_set.remove_file("little-waves.mp3")
    assert test_set.remove_file("waves-in-caves.wav", "individual_files")

    assert test_set.remove_file("", "") is False
    assert test_set.remove_file("", "individual_files") is False
    assert test_set.remove_file("little-waves.mp3", "") is False
    assert test_set.remove_file("invalid_name", "individual_files") is False
    assert test_set.remove_file("little-waves.mp3", "invalid_group") is False


def test_add_directory(setup):
    path, name, data_set = setup
    test_set = w_set.WorkingSet(True, data_set)

    assert test_set.add_directory("../../test_collection/water_sounds/", path + name, "individual_files")
    assert test_set.add_directory("../../test_collection/water_sounds/", path + name, "new_group")

    assert test_set.add_directory("", "", "") is False
    assert test_set.add_directory("", path + name, "individual_files") is False
    assert test_set.add_directory("../../test_collection/water_sounds/", "", "individual_files") is False
    assert test_set.add_directory("../../test_collection/water_sounds/", path + name, "") is False
    assert test_set.add_directory("invalid_path", path + name, "individual_files") is False
    assert test_set.add_directory("../../test_collection/water_sounds/", "invalid_config_path",
                                  "individual_files") is False
