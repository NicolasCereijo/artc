from core.artc_errors.validations.path import check_path_accessible
from core.artc_configurations import read_config
from pydub.utils import mediainfo


def get_extension(file: str):
    parts = file.split('.')

    if len(parts) > 1:
        extension = parts[-1].lower()
        return extension


def check_audio_corruption(file_path: str):
    """
        Function to check the readability of the file.

        Args:
            file_path (str): Path to the file with its name and extension included.

        Raises:
            True: If there were no problems reading.
            ValueError: If there were problems reading.
    """
    try:
        open(file_path, 'rb').read()
        return True
    except Exception:
        raise ValueError(f"Audio file '{file_path}' is corrupted")


def check_audio_format(path: str, name: str, configuration_path):
    """
        Function to check if the file extension is within the list of valid extensions.

        Args:
            path (str): Path or web address to the file.
            name (str): File name with extension.
            configuration_path (str): Path to the configuration file, automatically assigned to the default value.

        Raises:
            True: If the file format is valid.
            ValueError: If the file format is invalid.
    """
    file_extension = get_extension(name)

    check_audio_corruption(path + name)

    check_path_accessible(configuration_path)
    if file_extension not in read_config("extensions", configuration_path):
        raise ValueError(f"Invalid file format for '{name}'")
    return True
