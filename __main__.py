import os
import sys

import importlib.resources

import core


def main():
    configuration_path = str(importlib.resources.files('core.configurations') /
                             'default_configurations.json')
    logger = core.errors.logger_config.LoggerSingleton().get_logger()

    logger.info("Starting the ARtC suite...\n\n" +
                "    |     '||''|.     .     ..|'''.|      .|'''.|            ||    .          \n" +
                "   |||     ||   ||  .||.  .|'      '      ||..  '  ... ...  ...  .||.    .... \n" +
                "  |  ||    ||''|'    ||   ||               ''|||.   ||  ||   ||   ||   .|...||\n" +
                " .''''|.   ||   |.   ||   '|.      .     .     '||  ||  ||   ||   ||   ||     \n" +
                ".|.  .||. .||.  '|' .||.   ''|....'      |'....|'   '|..'|. .||.  '|.'  '|...'\n")

    if not os.access(configuration_path, os.R_OK):
        logger.critical("Could not access configuration file, suite execution aborted. The\n"
                        "default_configurations.json file should be located in the\n"
                        "/core/configurations/ folder. Check the directory and access permissions.")
        sys.exit(1)

    core.tests.main()


if __name__ == "__main__":
    main()
