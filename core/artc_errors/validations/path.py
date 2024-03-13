import requests.exceptions
import os.path


def check_url_reachable(url: str):
    """
        Function to check if the URL is reachable.

        Args:
            url (str): URL to check.

        Returns:
            True: If the URL is reachable.
        Raises:
            ValueError: If the URL is not reachable.
    """
    try:
        requests.get(url).raise_for_status()
        return True
    except requests.exceptions.RequestException:
        raise ValueError(f"URL '{url}' cannot be reached")


def check_path_accessible(path: str):
    """
        Function to check if the path is accessible.

        Args:
            path (str): Path to check.

        Returns:
            True: If the path is accessible.
        Raises:
            ValueError: If the path is not accessible.
    """
    if not os.path.exists(path):
        raise ValueError(f"Path '{path}' does not exist or is not accessible")
    return True


def check_file_readable(path: str, name: str):
    """
        Function to check if the file is readable.

        Args:
            path (str): Path to the file.
            name (str): File name with extension.

        Returns:
            True: If the file is readable.
        Raises:
            ValueError: If the file is not readable.
    """
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

        Returns:
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
