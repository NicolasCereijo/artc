import core.errors as errors
import importlib.resources
import pytest


@pytest.fixture()
def setup():
    configuration_path = str(importlib.resources.path('core.configurations', '')) + '/'
    ambient_sounds_path = str(importlib.resources.path('test_collection.ambient_sounds', '')) + '/'
    fire_sounds_path = str(importlib.resources.path('test_collection.fire_sounds', '')) + '/'

    return configuration_path, "default_configurations.json", ambient_sounds_path, fire_sounds_path


# ----------------------------------------------------------------------------------------------------------------------
# Tests for core.errors.validations.file
# ----------------------------------------------------------------------------------------------------------------------
def test_get_extension():
    assert errors.get_extension("file.mp3") == "mp3"
    assert errors.get_extension("file.wav") == "wav"

    assert errors.get_extension("file") is None
    assert errors.get_extension("") is None


def test_check_audio_format(setup):
    path, name, ambient_sounds_path, fire_sounds_path = setup
    configuration_file = path + name

    assert errors.check_audio_format(path=ambient_sounds_path, name="Desert Howling Wind.mp3",
                                     configuration_path=configuration_file)
    assert errors.check_audio_format(path=fire_sounds_path, name="Burning-fireplace.wav",
                                     configuration_path=configuration_file)

    assert errors.check_audio_format(path="", name="", configuration_path=configuration_file) is False
    assert errors.check_audio_format(path="", name="invalid_file", configuration_path=configuration_file) is False
    assert errors.check_audio_format(path="", name="invalid_file.pdf", configuration_path=configuration_file) is False
    assert errors.check_audio_format(path=ambient_sounds_path, name="invalid_file",
                                     configuration_path=configuration_file) is False


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
    path, name, _, _ = setup
    configuration_file = path + name

    assert errors.check_path_accessible(configuration_file)

    assert errors.check_path_accessible("") is False
    assert errors.check_path_accessible("invalid_path") is False


def test_check_file_readable(setup):
    path, name, _, _ = setup

    assert errors.check_file_readable(path=path, name=name)

    assert errors.check_file_readable(path="", name=name) is False
    assert errors.check_file_readable(path="invalid_path", name=name) is False
    assert errors.check_file_readable(path=path, name="") is False
    assert errors.check_file_readable(path=path, name="invalid_name") is False


@pytest.mark.skipif(not errors.check_url_reachable("https://www.google.com/"),
                    reason="This test requires an internet connection to run")
def test_validate_path(setup):
    path, name, _, _ = setup
    url_message_error = "\nIMPORTANT: Access to a test static URL has failed, check if this URL is still accessible"

    assert errors.validate_path(path=path, name=name)

    assert errors.validate_path(path="", name="") is False
    assert errors.validate_path(path="", name=name) is False
    assert errors.validate_path(path="invalid_path", name=name) is False
    assert errors.validate_path(path=path, name="") is False
    assert errors.validate_path(path="", name="invalid_name") is False
    assert errors.validate_path(path="https://invalid_url", name="") is False
    assert errors.validate_path(path="https://invalid_url", name="invalid_file") is False

    try:
        assert errors.validate_path(path="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/", name="bootstrap.css")
    except Exception as ex:
        print(url_message_error)
        raise ex
