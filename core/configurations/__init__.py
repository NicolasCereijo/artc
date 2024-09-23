import core.errors as errors
from pathlib import Path
import json

logger = errors.logger_config.LoggerSingleton().get_logger()


def open_config(configuration_path: Path) -> dict:
    try:
        if errors.check_path_accessible(configuration_path.parent) and configuration_path.is_file():
            with configuration_path.open('r') as file:
                return json.load(file)
    except ValueError:
        logger.critical("Could not access or parse configuration file")


def read_config(config_section: str, configuration_path: Path) -> dict:
    """
        Read and retrieve configuration settings from a specified section of a configuration file.

        Args:
            config_section (str): The section of the configuration file to read.
            configuration_path (Path): The path to the configuration file.

        Returns:
            dict: A dictionary containing the configuration settings for the specified section.
            None: If the specified section does not exist.

        Note:
            This function assumes that the configuration file follows a specific structure where 'audio'
            is a section containing various settings. It returns different parts of the 'audio' section
            based on the provided `config_section`. If the specified section or the configuration file
            itself does not exist, appropriate error messages are logged.
    """
    config = open_config(configuration_path)

    if config is not None:
        cases = {
            "all": config.get("audio", {}),
            "extensions": config.get("audio", {}).get("valid_extensions", [])
        }

        case_function = cases.get(config_section)
        if case_function is not None:
            return case_function
        else:
            logger.error("The specified section of the configuration file does not exist.")

    else:
        logger.critical("Error, configuration file does not exist or is not accessible. \nA "
                        "configuration file is required to run the program.")
