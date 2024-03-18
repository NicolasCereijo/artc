import core.artc_collections.working_set as w_set
import core.artc_analysis as analysis
import os


def main():
    configuration_path = "artc_configurations/configurations.json"
    print("========================== Starting the ARtC suite... ==========================")

    if os.access("artc_configurations/configurations.json", os.R_OK):
        example_set = w_set.WorkingSet()
        example_set.add_file("../test_collection/water_sounds/",
                             "little-waves.mp3", configuration_path)
        example_set.add_file("../test_collection/water_sounds/",
                             "waves-in-caves.wav", configuration_path)

        audio_signal_1 = example_set.__getitem__("little-waves.mp3")
        audio_signal_2 = example_set.__getitem__("waves-in-caves.wav")

        print(f"ZCR de la señal 1 consigo misma: {analysis.compare_zcr(audio_signal_1, audio_signal_1)}")
        print(f"ZCR de la señal 2 consigo misma: {analysis.compare_zcr(audio_signal_2, audio_signal_2)}")
        print(f"ZCR entre las señales 1 y 2: {analysis.compare_zcr(audio_signal_1, audio_signal_2)}")
        print(f"ZCR entre las señales 2 y 1: {analysis.compare_zcr(audio_signal_2, audio_signal_1)}")
    else:
        print("========= Could not access configuration file, suite execution aborted =========\n"
              "The configurations.json file should be located in the /core/artc_configurations/\n"
              "folder. Check the directory and access permissions.")


if __name__ == "__main__":
    main()
