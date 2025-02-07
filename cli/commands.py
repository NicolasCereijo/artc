import os
import sys
import argparse
import json
import importlib.resources
from logging import Logger
from typing import List

from core import tests


def about() -> None:
    print("""
        ARtC (Audio Real-time Comparator)
        ================================

        ARtC is a software suite designed to compare and analyze audio files in real time.

        Version: 1.0b4
        Author: Nicolás Cereijo Ranchal
        Author Email: nicolascereijoranchal@gmail.com
        URL: https://github.com/NicolasCereijo/artc
        License: MIT

        Development Status:
        -------------------
        This project is currently in active development. The goal is to provide a reliable tool
        for real-time audio comparison, but certain features may still be under testing or not
        fully stable.
        """)


def load_commands(commands_path: str, *, logger: Logger) -> List[str]:
    try:
        with open(commands_path, "r") as file:
            config = json.load(file)
            return config.get('commands', [])
    except FileNotFoundError:
        logger.warning("The commands.json file was not found, a default list of commands is\nbeing "
                       "used instead")
        return ["welcome", "test"]


def parse_args(commands_path: str, *, logger: Logger) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Main argument parser for the ARtC suite")

    parser.add_argument(
        "command",
        choices=load_commands(commands_path, logger=logger),
        nargs="?",
        default="welcome",
        help="Primary command to execute. Valid options include the globally defined ARtC commands."
    )
    parser.add_argument(
        "command_args",
        nargs=argparse.REMAINDER,
        help="Optional additional arguments for the selected command, passed as-is to the handler."
    )

    return parser.parse_args()


def handle_command(command: str, *, command_args: list = [], logger: Logger) -> None:
    if command == "test":
        tests.main(command_args)

    elif command == "welcome":
        configuration_path = str(importlib.resources.files('core.configurations') /
                                 'default_configurations.json')

        logger.info("Starting the ARtC suite...\n\n" +
                    "    |     '||''|.     .     ..|'''.|      .|'''.|            ||    .          \n" +
                    "   |||     ||   ||  .||.  .|'      '      ||..  '  ... ...  ...  .||.    .... \n" +
                    "  |  ||    ||''|'    ||   ||               ''|||.   ||  ||   ||   ||   .|...||\n" +
                    " .''''|.   ||   |.   ||   '|.      .     .     '||  ||  ||   ||   ||   ||     \n" +
                    ".|.  .||. .||.  '|' .||.   ''|....'      |'....|'   '|..'|. .||.  '|.'  '|...'\n\n")
        about()

        if not os.access(configuration_path, os.R_OK):
            logger.critical("Could not access configuration file, suite execution aborted. The\n"
                            "default_configurations.json file should be located in the /core"
                            "/configurations/\nfolder. Check the directory and access permissions.")
            sys.exit(1)
