import core.artc_errors.validations.file as file_err
import core.artc_errors.validations.path as path_err
import os


class WorkingSet:
    def __init__(self):
        self.working_set = {"individual_files":  []}

    def search_file(self, name: str, group: str = "individual_files"):
        """
            Function to check the existence of a file within a group.

            Args:
                name (str): File name with extension.
                group (str): Group where the file should be.

            Raises:
                True: if the file is in the group.
                False: If the file is not found in the group.
        """
        if name not in [file_data['name'] for file_data in self.working_set[group]]:
            return False
        return True

    def add_file(self, path: str, name: str, configuration_path: str, group: str = "individual_files"):
        """
            Function to add files to a new or existing group.

            Args:
                path (str): Path or web address to the file.
                name (str): File name with extension.
                configuration_path (str): Path to the configuration file.
                group (str): Group to which the file will be added.

            Raises:
                True: If the file is accessible.
                False: If the file is not accessible.
        """
        try:
            file_err.check_audio_format(path, name, configuration_path)
        except ValueError as ve:
            print(ve)
            return False

        if path_err.validate_path(path, name):
            if group not in self.working_set:
                self.working_set[group] = []

            self.working_set[group].append({"path": path, "name": name})
            return True
        else:
            return False

    def remove_file(self, name: str, group: str = "individual_files"):
        """
            Function to delete files from a group.

            Args:
                name (str): File name with extension.
                group (str): Group from which the file will be deleted.

            Raises:
                True: If the file can be deleted.
                False: If the file cannot be deleted.
        """
        if group not in self.working_set or not self.search_file(name, group):
            return False
        else:
            for group in self.working_set:
                self.working_set[group] = list(filter(lambda file_data: file_data["name"] != name,
                                                      self.working_set[group]))
        return True

    def add_directory(self, path: str, configuration_path: str, group: str = "individual_files"):
        """
            Function to add all valid files in a directory to a group.

            Args:
                path (str): Path to the directory. Can not use a web address.
                configuration_path (str): Path to the configuration file.
                group (str): Group to which the files will be added.

            Raises:
                True: If any file could be added.
                False: If the directory could not be accessed or any files added.
        """
        any_files_added = False

        try:
            path_err.check_path_accessible(path)
        except ValueError as ve:
            print(ve)
            return False

        for name in os.listdir(path):
            if self.add_file(path, name, configuration_path, group):
                any_files_added = True

        return any_files_added
