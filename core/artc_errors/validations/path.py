import requests.exceptions
import os.path


def check_url_reachable(url: str):
    try:
        requests.get(url).raise_for_status()
        return True
    except requests.exceptions.RequestException:
        raise ValueError(f"URL '{url}' cannot be reached")


def check_path_accessible(path: str):
    if not os.path.exists(path):
        raise ValueError(f"Path '{path}' does not exist or is not accessible")
    return True


def check_file_readable(path: str, name: str):
    if name is None or name == "" or not os.access(os.path.join(path, name), os.R_OK):
        raise ValueError(f"File '{name}' is not accessible for reading")
    return True


def validate_path(path: str, name: str):
    """
        Function to check the validity of a path and the accessibility of the file.
        The file can be hosted locally or on the internet.

        Args:
            path (str): Path or web address to the file.
            name (str): File name with extension.

        Raises:
            True: If the file is accessible.
            False: If the file is not accessible.
    """
    try:
        if path.startswith("http"):
            check_url_reachable(path + name)
        else:
            check_path_accessible(path)
            check_file_readable(path, name)

    except ValueError as ve:
        print(ve)
        return False

    return True
