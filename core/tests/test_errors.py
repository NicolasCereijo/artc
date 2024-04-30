import core.errors as errors
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
    return "../configurations/", "default_configurations.json"


# ----------------------------------------------------------------------------------------------------------------------
# Tests for core.errors.validations.file
# ----------------------------------------------------------------------------------------------------------------------
def test_get_extension():
    assert errors.get_extension("file.mp3") == "mp3"
    assert errors.get_extension("file.wav") == "wav"

    assert errors.get_extension("file") is None
    assert errors.get_extension("") is None


def test_check_audio_format(setup):
    path, name = setup
    configuration_file = path + name

    assert errors.check_audio_format("../../test_collection/ambient_sounds/",
                                     "Desert Howling Wind.mp3", configuration_file)
    assert errors.check_audio_format("../../test_collection/fire_sounds/",
                                     "Burning-fireplace.wav", configuration_file)

    assert errors.check_audio_format("", "", configuration_file) is False
    assert errors.check_audio_format("", "invalid_file", configuration_file) is False
    assert errors.check_audio_format("", "invalid_file.pdf", configuration_file) is False
    assert errors.check_audio_format("../../test_collection/ambient_sounds/",
                                     "invalid_file", configuration_file) is False


# ----------------------------------------------------------------------------------------------------------------------
# Tests for core.errors.validations.path
# ----------------------------------------------------------------------------------------------------------------------
@pytest.mark.skipif(not errors.check_url_reachable("https://www.google.com/"),
                    reason="This test requires an internet connection to run")
def test_check_url_reachable():
    url_message_error = "\nIMPORTANT: Access to a test static URL has failed, check if this URL is still accessible"

    try:
        assert errors.check_url_reachable("https://www.google.com"), url_message_error
    except Exception as ex:
        print(url_message_error)
        raise ex

    assert errors.check_url_reachable("") is False
    assert errors.check_url_reachable("https://invalid_url") is False


def test_check_path_accessible(setup):
    path, name = setup
    configuration_file = path + name

    assert errors.check_path_accessible(configuration_file)

    assert errors.check_path_accessible("") is False
    assert errors.check_path_accessible("invalid_path") is False


def test_check_file_readable(setup):
    path, name = setup

    assert errors.check_file_readable(path, name)

    assert errors.check_file_readable("", name) is False
    assert errors.check_file_readable("invalid_path", name) is False
    assert errors.check_file_readable(path, "") is False
    assert errors.check_file_readable(path, "invalid_name") is False


@pytest.mark.skipif(not errors.check_url_reachable("https://www.google.com/"),
                    reason="This test requires an internet connection to run")
def test_validate_path(setup):
    path, name = setup
    url_message_error = "\nIMPORTANT: Access to a test static URL has failed, check if this URL is still accessible"

    assert errors.validate_path(path, name)

    assert errors.validate_path("", "") is False
    assert errors.validate_path("", name) is False
    assert errors.validate_path("invalid_path", name) is False
    assert errors.validate_path(path, "") is False
    assert errors.validate_path("", "invalid_name") is False
    assert errors.validate_path("https://invalid_url", "") is False
    assert errors.validate_path("https://invalid_url", "invalid_file") is False

    try:
        assert errors.validate_path("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/", "bootstrap.css")
    except Exception as ex:
        print(url_message_error)
        raise ex
