import pytest
from pathlib import Path

import core.configurations as config


@pytest.fixture()
def setup():
    current_path = Path(__file__)

    if current_path.parent.name == 'tests':
        config_path = current_path.parent.parent / 'configurations' / 'default_configurations.json'
    else:
        config_path = current_path.parent / 'configurations' / 'default_configurations.json'

    return config_path


def test_open_config(setup):
    configuration_file = setup

    assert config.open_config(configuration_file) is not None

    assert config.open_config(Path("")) is None
    assert config.open_config(Path("invalid_configuration_path")) is None
    assert config.open_config(Path("invalid_configuration_path.json")) is None


def test_read_config(setup):
    configuration_file = setup

    assert config.read_config("all", configuration_file) is not None
    assert config.read_config("extensions", configuration_file) is not None

    assert config.read_config("invalid_section", configuration_file) is None
    assert config.read_config("all", Path("invalid_configuration_path")) is None
