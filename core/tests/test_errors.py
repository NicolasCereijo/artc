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
        path: Relative path to the configuration file.
        name: Name of the configuration file.
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

    assert file_err.check_audio_format("valid_file.mp3", configuration_file) is True
    assert file_err.check_audio_format("valid_file.wav", configuration_file) is True

    with pytest.raises(ValueError):
        assert file_err.check_audio_format("", configuration_file) is ValueError

    with pytest.raises(ValueError):
        assert file_err.check_audio_format("invalid_file", configuration_file) is ValueError

    with pytest.raises(ValueError):
        assert file_err.check_audio_format("invalid_file.pdf", configuration_file) is ValueError

    with pytest.raises(ValueError):
        assert file_err.check_audio_format("valid_file.mp3", "invalid_path") is ValueError


# ----------------------------------------------------------------------------------------------------------------------
# Tests for core.artc_errors.validations.path
# ----------------------------------------------------------------------------------------------------------------------
def test_check_url_reachable():
    assert path_err.check_url_reachable("https://www.google.com") is True

    with pytest.raises(ValueError):
        assert path_err.check_url_reachable("") is ValueError

    with pytest.raises(ValueError):
        assert path_err.check_url_reachable("https://invalid_url") is ValueError


def test_check_path_accessible(setup):
    path, name = setup
    configuration_file = path + name

    assert path_err.check_path_accessible(configuration_file) is True

    with pytest.raises(ValueError):
        assert path_err.check_path_accessible("") is ValueError

    with pytest.raises(ValueError):
        assert path_err.check_path_accessible("invalid_path") is ValueError


def test_check_file_readable(setup):
    path, name = setup

    assert path_err.check_file_readable(path, name) is True

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

    assert path_err.validate_path(path, name) is True

    assert path_err.validate_path("", name) is False
    assert path_err.validate_path("invalid_path", name) is False
    assert path_err.validate_path(path, "") is False
    assert path_err.validate_path("", "invalid_name") is False
