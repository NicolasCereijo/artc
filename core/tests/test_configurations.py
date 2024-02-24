import core.artc_configurations as config
import pytest


def test_open_config():
    assert config.open_config("../artc_configurations/configurations.json") is not None


def test_check_config_all():
    assert config.read_config("../artc_configurations/configurations.json", "all") is not None


def test_check_config_extensions():
    assert config.read_config("../artc_configurations/configurations.json", "extensions") is not None


def test_check_config_invalid_section():
    with pytest.raises(ValueError):
        config.read_config("../artc_configurations/configurations.json", "invalid")
