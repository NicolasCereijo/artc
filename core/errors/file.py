import core.errors as errors
import core.configurations as config
import os


def get_extension(file: str) -> str:
    parts = file.split('.')

    if len(parts) > 1:
        extension = parts[-1].lower()
        return extension


def check_audio_corruption(file_path: str) -> bool:
    try:
        open(file_path, 'rb').read()
        return True
    except (FileNotFoundError, PermissionError, IsADirectoryError, OSError):
        return False


def check_audio_format(*, path: str, name: str, configuration_path: str) -> bool:
    if (not check_audio_corruption(path + name)
            or not errors.check_path_accessible(configuration_path)
            or not (os.path.isfile(os.path.join(path, name))
                    or get_extension(name) not in config.read_config("extensions", configuration_path))):
        return False
    return True
