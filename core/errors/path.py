import requests.exceptions
import os.path


def check_url_reachable(url: str) -> bool:
    try:
        requests.get(url).raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False


def check_path_accessible(path: str) -> bool:
    if not os.path.exists(path):
        return False
    return True


def check_file_readable(path: str, name: str) -> bool:
    if name is None or name == "" or not os.access(os.path.join(path, name), os.R_OK):
        return False
    return True


def validate_path(path: str, name: str) -> bool:
    if ((path.startswith("http") and check_url_reachable(path + name))
            or (check_path_accessible(path) and check_file_readable(path, name))):
        return True
    return False
