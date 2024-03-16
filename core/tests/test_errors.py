import core.artc_errors.validations.file as file_err
import core.artc_errors.validations.path as path_err
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
    """
    return "../artc_configurations/", "configurations.json"


# ----------------------------------------------------------------------------------------------------------------------
# Tests for core.artc_errors.validations.file
# ----------------------------------------------------------------------------------------------------------------------
def test_get_extension():
    assert file_err.get_extension("file.mp3") == "mp3"
    assert file_err.get_extension("file.wav") == "wav"

    assert file_err.get_extension("file") is None
    assert file_err.get_extension("") is None


def test_check_audio_format(setup):
    path, name = setup
    configuration_file = path + name

    assert file_err.check_audio_format("../../test_collection/ambient_sounds/",
                                       "Desert Howling Wind.mp3", configuration_file)
    assert file_err.check_audio_format("../../test_collection/fire_sounds/",
                                       "Burning-fireplace.wav", configuration_file)

    with pytest.raises(ValueError):
        assert file_err.check_audio_format("", "", configuration_file) is ValueError

    with pytest.raises(ValueError):
        assert file_err.check_audio_format("", "invalid_file", configuration_file) is ValueError

    with pytest.raises(ValueError):
        assert file_err.check_audio_format("", "invalid_file.pdf", configuration_file) is ValueError

    with pytest.raises(ValueError):
        assert file_err.check_audio_format("../../test_collection/ambient_sounds/",
                                           "invalid_file", configuration_file) is ValueError


# ----------------------------------------------------------------------------------------------------------------------
# Tests for core.artc_errors.validations.path
# ----------------------------------------------------------------------------------------------------------------------
def test_check_url_reachable():
    url_message_error = "\nIMPORTANT: Access to a test static URL has failed, check if this URL is still accessible"

    try:
        assert path_err.check_url_reachable("https://www.google.com"), url_message_error
    except Exception as ex:
        print(url_message_error)
        raise ex

    with pytest.raises(ValueError):
        assert path_err.check_url_reachable("") is ValueError

    with pytest.raises(ValueError):
        assert path_err.check_url_reachable("https://invalid_url") is ValueError


def test_check_path_accessible(setup):
    path, name = setup
    configuration_file = path + name

    assert path_err.check_path_accessible(configuration_file)

    with pytest.raises(ValueError):
        assert path_err.check_path_accessible("") is ValueError

    with pytest.raises(ValueError):
        assert path_err.check_path_accessible("invalid_path") is ValueError


def test_check_file_readable(setup):
    path, name = setup

    assert path_err.check_file_readable(path, name)

    with pytest.raises(ValueError):
        assert path_err.check_file_readable("", name) is ValueError

    with pytest.raises(ValueError):
        assert path_err.check_file_readable("invalid_path", name) is ValueError

    with pytest.raises(ValueError):
        assert path_err.check_file_readable(path, "") is ValueError

    with pytest.raises(ValueError):
        assert path_err.check_file_readable(path, "invalid_name") is ValueError


def test_validate_path(setup):
    path, name = setup
    url_message_error = "\nIMPORTANT: Access to a test static URL has failed, check if this URL is still accessible"

    assert path_err.validate_path(path, name)
    assert path_err.validate_path("", "") is False
    assert path_err.validate_path("", name) is False
    assert path_err.validate_path("invalid_path", name) is False
    assert path_err.validate_path(path, "") is False
    assert path_err.validate_path("", "invalid_name") is False
    assert path_err.validate_path("https://invalid_url", "") is False
    assert path_err.validate_path("https://invalid_url", "invalid_file") is False

    try:
        assert path_err.validate_path("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/",
                                      "bootstrap.min.css"), url_message_error
    except Exception as ex:
        print(url_message_error)
        raise ex
