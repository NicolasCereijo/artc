import json
import os


def open_config(configuration_path: str):
    """
        Function to access configuration file path.

        Args:
            configuration_path (str): The parameter value indicates the path of the configuration file:
                - empty: Use the default path.
    """
    try:
        if os.access(configuration_path, os.R_OK):
            with open(configuration_path, 'r') as file:
                return json.load(file)
    except ValueError:
        print("Could not access file")


def read_config(config_section, configuration_path: str):
    """
        Function to read the configuration file.

        Args:
            config_section (str): The parameter value indicates the section of the configuration returned:
                - 'all': Returns the entire file.
                - 'extensions': Returns valid extensions for files.
            configuration_path (str): The parameter value indicates the path of the configuration file:
                - empty: Use the default path.

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
            print("The specified section of the configuration file does not exist.")

    else:
        print("Error, configuration file does not exist or is not accessible. \nA "
              "configuration file is required to run the program.")
