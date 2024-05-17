import core.configurations as config
import importlib.resources
import pytest


@pytest.fixture()
def setup():
    return str(importlib.resources.files('core.configurations') / 'default_configurations.json')


def test_open_config(setup):
    configuration_file = setup

    assert config.open_config(configuration_file) is not None

    assert config.open_config("") is None
    assert config.open_config("invalid_configuration_path") is None


def test_read_config(setup):
    configuration_file = setup

    assert config.read_config("all", configuration_file) is not None
    assert config.read_config("extensions", configuration_file) is not None

    assert config.read_config("invalid_section", configuration_file) is None
    assert config.read_config("all", "invalid_configuration_path") is None
