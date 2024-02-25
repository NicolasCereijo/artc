import core.artc_configurations as config


def test_open_config():
    assert config.open_config("../artc_configurations/configurations.json") is not None

    assert config.open_config("") is None
    assert config.open_config("invalid_configuration_path") is None


def test_read_config():
    assert config.read_config("all", "../artc_configurations/configurations.json") is not None
    assert config.read_config("extensions", "../artc_configurations/configurations.json") is not None

    assert config.read_config("invalid_section", "../artc_configurations/configurations.json") is None
    assert config.read_config("all", "invalid_configuration_path") is None
