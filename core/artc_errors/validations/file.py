from core.artc_errors.validations.path import check_path_accessible
from core.artc_configurations import read_config
from pydub.utils import mediainfo


def get_extension(file):
    parts = file.split('.')

    if len(parts) > 1:
        extension = parts[-1].lower()
        return extension


def check_audio_format(name, configuration_path="default"):
    """
        Function to check if the file extension is within the list of valid extensions.

        Args:
            name (str): File name with extension.
            configuration_path (str): Path to the configuration file, automatically assigned to the default value.

        Raises:
            True: If the file format is valid
            ValueError: If the file format is invalid
    """
    file_extension = get_extension(name)

    check_path_accessible(configuration_path)

    if file_extension not in read_config("extensions", configuration_path):
        raise ValueError("Invalid file format")
    return True


def check_audio_corruption(file_path):
    try:
        mediainfo(file_path)
    except Exception as ex:
        raise ValueError(f"Audio file '{file_path}' is corrupted: {ex}")

    return True
