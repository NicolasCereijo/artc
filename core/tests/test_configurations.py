import core.configurations as config
import pytest


def test_open_config():
    assert config.open_config("../configurations/configurations.json") is not None


def test_check_config_all():
    assert config.read_config("../configurations/configurations.json", "all") is not None


def test_check_config_extensions():
    assert config.read_config("../configurations/configurations.json", "extensions") is not None


def test_check_config_invalid_section():
    with pytest.raises(ValueError):
        config.read_config("../configurations/configurations.json", "invalid")
