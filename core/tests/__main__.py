import os
import sys
import importlib.resources
import pytest

from .. import errors


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    configuration_path = str(importlib.resources.files('core.configurations') /
                             'default_configurations.json')
    logger = errors.logger_config.LoggerSingleton().get_logger()

    logger.info("Running the main test suite for ARtC...\n\n" +
                "    |     '||''|.     .     ..|'''.|      .|'''.|            ||    .          \n" +
                "   |||     ||   ||  .||.  .|'      '      ||..  '  ... ...  ...  .||.    .... \n" +
                "  |  ||    ||''|'    ||   ||               ''|||.   ||  ||   ||   ||   .|...||\n" +
                " .''''|.   ||   |.   ||   '|.      .     .     '||  ||  ||   ||   ||   ||     \n" +
                ".|.  .||. .||.  '|' .||.   ''|....'      |'....|'   '|..'|. .||.  '|.'  '|...'\n")

    logger.info(
        "Technical note: Libraries aifc, audioop, and sunau have deprecation\n" +
        "warnings for Python 3.13. This is a known issue dependent on third-party\n" +
        "libraries. If these libraries are not updated and a migration to Python 3.13\n" +
        "is considered in a future version, alternatives to the current libraries will\n" +
        "be explored.\n")

    if os.access(configuration_path, os.R_OK):
        result = pytest.main(args)

        if result == 0:
            logger.info("All executed tests were successful")
        else:
            logger.error("Bugs were found in the test set during execution")
    else:
        logger.critical("Could not access configuration file, suite execution aborted. The\n"
                        "default_configurations.json file should be located in the /core"
                        "/configurations/\nfolder. Check the directory and access permissions.")
        sys.exit(1)
