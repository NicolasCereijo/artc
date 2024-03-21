import core.artc_errors.logger_config as log
import json
import os


def open_config(configuration_path: str):
    logger = log.LoggerSingleton().get_logger()

    try:
        if os.access(configuration_path, os.R_OK):
            with open(configuration_path, 'r') as file:
                return json.load(file)
    except ValueError:
        logger.critical("Could not access configuration file")


def read_config(config_section: str, configuration_path: str):
    logger = log.LoggerSingleton().get_logger()
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
