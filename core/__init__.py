import core.artc_collections.working_set as set
import os


def main():
    configuration_path = "artc_configurations/configurations.json"
    print("========================== Starting the ARtC suite... ==========================")

    if os.access("artc_configurations/configurations.json", os.R_OK):
        ejemplo = set.WorkingSet()
        ejemplo.add_file("/home/nico/Música/Investigación/Colección sonidos investigación/Sonidos de agua/",
                         "little-waves.mp3", configuration_path)
        print(ejemplo.working_set)
        ejemplo.remove_file("little-waves.mp3")
        print(ejemplo.working_set)
        ejemplo.add_directory("/home/nico/Música/Investigación/Colección sonidos investigación/Sonidos de agua/",
                              configuration_path)
        print(ejemplo.working_set)
    else:
        print("========= Could not access configuration file, suite execution aborted =========\n"
              "The configurations.json file should be located in the /core/artc_configurations/\n"
              "folder. Check the directory and access permissions.")


if __name__ == "__main__":
    main()
