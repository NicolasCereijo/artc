import requests.exceptions
import os.path


def check_url_reachable(url):
    try:
        requests.get(url).raise_for_status()
    except requests.exceptions.RequestException as ex:
        raise ValueError(f"URL '{url}' cannot be reached: {ex}")


def check_path_accessible(path):
    if not os.path.exists(path):
        raise ValueError(f"Path '{path}' does not exist or is not accessible")


def check_file_readable(address, name):
    if not os.access(os.path.join(address, name), os.R_OK):
        raise ValueError(f"File '{name}' is not accessible for reading")


def validate_path(address, name):
    try:
        if address.startswith("http"):
            check_url_reachable(address)
        else:
            check_path_accessible(address)

        check_file_readable(address, name)
    except ValueError as ex:
        print(ex)

    return True
