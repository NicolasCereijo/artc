import os


def main():
    print("========================== Starting the ARtC suite... ==========================")

    if os.access("artc_configurations/configurations.json", os.R_OK):
        print("potato")
    else:
        print("========= Could not access configuration file, suite execution aborted =========\n"
              "The configurations.json file should be located in the /core/artc_configurations/\n"
              "folder. Check the directory and access permissions.")


if __name__ == "__main__":
    main()
