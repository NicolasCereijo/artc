import core.artc_errors as err
import librosa
import os


class WorkingSet:
    def __init__(self, test_mode: bool = False, data_set: dict = None):
        """
            Function to initialize instances of the class.
            Test mode available, disabled by default.

            Args:
                test_mode (bool, optional): True to use test mode.
                data_set (dict, optional): Data set to perform the tests. Required if test_mode is True.
        """
        if not test_mode:
            self.working_set = {"individual_files":  []}
        else:
            self.working_set = data_set

    def __getitem__(self, name: str, group: str = "individual_files"):
        """
            Retrieve the audio signal corresponding to the given file name from the specified group.

            Args:
                name (str): The name of the file to retrieve.
                group (str, optional): The name of the group containing the file, 'individual_files' by default.

            Returns:
                The audio signal associated with the file name.
            Raises:
                KeyError: If the file with the given name is not found in the specified group.
        """
        for file in self.working_set[group]:
            if file["name"] == name:
                return file["audio_signal"]
        raise KeyError(f"No file with name '{name}' was found in key '{group}'")

    def __contains__(self, name: str, group: str = "individual_files"):
        """
            Function to check the existence of a file within a group.

            Args:
                name (str): File name with extension.
                group (str, optional): Group where the file should be.

            Returns:
                True: if the file is in the group.
                False: If the file is not found in the group.
        """
        if (group not in self.working_set or
                name not in [file_name['name'] for file_name in self.working_set[group]]):
            return False
        return True

    def add_file(self, path: str, name: str, configuration_path: str, group: str = "individual_files"):
        """
            Function to add files to a new or existing group.

            Args:
                path (str): Path or web address to the file.
                name (str): File name with extension.
                configuration_path (str): Path to the configuration file.
                group (str, optional): Group to which the file will be added.

            Returns:
                True: If the file is accessible.
                False: If the file is not accessible.
        """
        try:
            err.check_audio_format(path, name, configuration_path)
        except ValueError as ve:
            print(ve)
            return False

        if err.validate_path(path, name) and group != "":
            if group not in self.working_set:
                self.working_set[group] = []

            audio_signal, sample_rate = librosa.load(path + name)
            self.working_set[group].append({"path": path, "name": name,
                                            "audio_signal": audio_signal, "sample_rate": sample_rate})
            return True
        else:
            return False

    def remove_file(self, name: str, group: str = "individual_files"):
        """
            Function to delete files from a group.

            Args:
                name (str): File name with extension.
                group (str, optional): Group from which the file will be deleted.

            Returns:
                True: If the file can be deleted.
                False: If the file cannot be deleted.
        """
        if not self.__contains__(name, group):
            return False
        else:
            for group in self.working_set:
                # Create a list excluding the file to delete
                self.working_set[group] = list(filter(lambda file_data:
                                                      file_data["name"] != name, self.working_set[group]))
        return True

    def add_directory(self, path: str, configuration_path: str, group: str = "individual_files"):
        """
            Function to add all valid files in a directory to a group.

            Args:
                path (str): Path to the directory. Can not use a web address.
                configuration_path (str): Path to the configuration file.
                group (str, optional): Group to which the files will be added.

            Returns:
                True: If any file could be added.
                False: If the directory could not be accessed or any files added.
        """
        any_files_added = False

        try:
            err.check_path_accessible(path)
            err.check_path_accessible(configuration_path)
        except ValueError as ve:
            print(ve)
            return False

        for name in os.listdir(path):
            if self.add_file(path, name, configuration_path, group):
                any_files_added = True

        return any_files_added
