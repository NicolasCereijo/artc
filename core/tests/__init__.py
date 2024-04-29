from core.tests import *
import core.errors as errors
import pytest
import os


def main():
    logger = errors.logger_config.LoggerSingleton().get_logger()

    logger.info("Running the main test suite for ARtC...\n\n" +
                "    |     '||''|.     .     ..|'''.|       .|'''.|            ||    .          \n" +
                "   |||     ||   ||  .||.  .|'      '       ||..  '  ... ...  ...  .||.    .... \n" +
                "  |  ||    ||''|'    ||   ||                ''|||.   ||  ||   ||   ||   .|...||\n" +
                " .''''|.   ||   |.   ||   '|.      .      .     '||  ||  ||   ||   ||   ||     \n" +
                ".|.  .||. .||.  '|' .||.   ''|....'       |'....|'   '|..'|. .||.  '|.'  '|...'\n")

    if os.access("../configurations/configurations.json", os.R_OK):
        result = pytest.main()

        if result == 0:
            logger.info("All tests ran successfully")
        else:
            logger.error("Bugs were found in the test set during execution")
    else:
        logger.critical("Could not access configuration file, suite execution aborted. The\n"
                        "configurations.json file should be located in the /core/configurations/\n"
                        "folder. Check the directory and access permissions.")


if __name__ == "__main__":
    main()
