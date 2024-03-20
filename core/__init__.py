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

        print("Zero Crossing Rate:")
        print(f"ZCR of signal 1 with itself: {analysis.compare_zcr(audio_signal_1, audio_signal_1)}")
        print(f"ZCR of signal 2 with itself: {analysis.compare_zcr(audio_signal_2, audio_signal_2)}")
        print(f"ZCR between signals 1 and 2: {analysis.compare_zcr(audio_signal_1, audio_signal_2)}")
        print(f"ZCR between signals 2 and 1: {analysis.compare_zcr(audio_signal_2, audio_signal_1)}\n")

        print("Espectrograms comparison:")
        print(f"Espectrogram comparison of signal 1 with itself: "
              f"{analysis.compare_two_spectrograms(audio_signal_1, audio_signal_1)}")
        print(f"Espectrogram comparison of signal 2 with itself: "
              f"{analysis.compare_two_spectrograms(audio_signal_2, audio_signal_2)}")
        print(f"Espectrogram comparison between signals 1 and 2: "
              f"{analysis.compare_two_spectrograms(audio_signal_1, audio_signal_2)}")
        print(f"Espectrogram comparison between signals 2 and 1: "
              f"{analysis.compare_two_spectrograms(audio_signal_2, audio_signal_1)}")
    else:
        print("========= Could not access configuration file, suite execution aborted =========\n"
              "The configurations.json file should be located in the /core/artc_configurations/\n"
              "folder. Check the directory and access permissions.")


if __name__ == "__main__":
    main()
