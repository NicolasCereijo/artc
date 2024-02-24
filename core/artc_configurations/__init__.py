import json
import os


def open_config(configuration_path):
    """
        Method to access configuration file path.

        Args:
            configuration_path (str): The parameter value indicates the path of the configuration file:
                - default: Use the default path.

        """
    configuration_file = "core/artc_configurations/artc_configurations.json"

    if configuration_path != "default":
        configuration_file = configuration_path

    if os.access(configuration_file, os.R_OK):
        with open(configuration_file, 'r') as file:
            return json.load(file)
    return None


def read_config(configuration_path, config_section):
    """
        Method to read the configuration file.

        Args:
            configuration_path (str): The parameter value indicates the path of the configuration file:
                - default: Use the default path.
            config_section (str): The parameter value indicates the section of the configuration returned:
                - 'all': Returns the entire file.
                - 'extensions': Returns valid extensions for files.

        Raises:
            ValueError: If the parameter is not in the options list.

        """
    config = open_config(configuration_path)

    if config is not None:
        # Select the section of the configuration file to return
        cases = {
            "all": config.get("audio", {}),
            "extensions": config.get("audio", {}).get("valid_extensions", [])
        }

        case_function = cases.get(config_section)
        if case_function is not None:
            return case_function
        else:
            raise ValueError("The specified section of the configuration file does not exist.")

    else:
        raise ValueError("Error, configuration file does not exist or is not accessible. "
                         "\nA configuration file is required to run the program.")
