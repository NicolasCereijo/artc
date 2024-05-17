from core.tests import *
import core.errors as errors
import importlib.resources
import pytest
import os


def main():
    configuration_path = str(importlib.resources.files('core.configurations') / 'default_configurations.json')
    logger = errors.logger_config.LoggerSingleton().get_logger()

    logger.info("Running the main test suite for ARtC...\n" +
                "If internet access is not possible some tests will be skipped\n\n" +
                "    |     '||''|.     .     ..|'''.|       .|'''.|            ||    .          \n" +
                "   |||     ||   ||  .||.  .|'      '       ||..  '  ... ...  ...  .||.    .... \n" +
                "  |  ||    ||''|'    ||   ||                ''|||.   ||  ||   ||   ||   .|...||\n" +
                " .''''|.   ||   |.   ||   '|.      .      .     '||  ||  ||   ||   ||   ||     \n" +
                ".|.  .||. .||.  '|' .||.   ''|....'       |'....|'   '|..'|. .||.  '|.'  '|...'\n")

    if os.access(configuration_path, os.R_OK):
        result = pytest.main()

        if result == 0:
            logger.info("All executed tests were successful")
        else:
            logger.error("Bugs were found in the test set during execution")
    else:
        logger.critical("Could not access configuration file, suite execution aborted. The\n"
                        "default_configurations.json file should be located in the /core/configurations/\n"
                        "folder. Check the directory and access permissions.")


if __name__ == "__main__":
    main()
