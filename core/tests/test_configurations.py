import core.configurations as config
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
    return "../configurations/", "configurations.json"


def test_open_config(setup):
    path, name = setup
    configuration_file = path + name

    assert config.open_config(configuration_file) is not None

    assert config.open_config("") is None
    assert config.open_config("invalid_configuration_path") is None


def test_read_config(setup):
    path, name = setup
    configuration_file = path + name

    assert config.read_config("all", configuration_file) is not None
    assert config.read_config("extensions", configuration_file) is not None

    assert config.read_config("invalid_section", configuration_file) is None
    assert config.read_config("all", "invalid_configuration_path") is None
