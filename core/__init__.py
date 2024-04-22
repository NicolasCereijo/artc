import core.artc_collections.working_set as w_set
import core.artc_analysis as analysis
import core.artc_errors as err
import logging
import os


def main():
    configuration_path = "artc_configurations/configurations.json"
    logger = err.logger_config.LoggerSingleton().get_logger()

    logger.info("Starting the ARtC suite...\n\n" +
                "    |     '||''|.     .     ..|'''.|       .|'''.|            ||    .          \n" +
                "   |||     ||   ||  .||.  .|'     '        ||..  '  ... ...  ...  .||.    .... \n" +
                "  |  ||    ||''|'    ||   ||                ''|||.   ||  ||   ||   ||   .|...||\n" +
                " .''''|.   ||   |.   ||   '|.      .      .     '||  ||  ||   ||   ||   ||     \n" +
                ".|.  .||. .||.  '|' .||.   ''|....'       |'....|'   '|..'|. .||.  '|.'  '|...'\n")

    if os.access(configuration_path, os.R_OK):
        example_set = w_set.WorkingSet()
        example_set.add_file("../test_collection/water_sounds/",
                             "little-waves.mp3", configuration_path)
        example_set.add_file("../test_collection/water_sounds/",
                             "waves-in-caves.wav", configuration_path)

        audio_signal_1, sample_rate1 = example_set.__getitem__("little-waves.mp3")
        audio_signal_2, sample_rate2 = example_set.__getitem__("waves-in-caves.wav")

        print("Chroma comparison:")
        print(f"Chroma of signal 1 with it self: "
              f"{analysis.compare_two_chroma(audio_signal_1, audio_signal_1, sample_rate1, sample_rate1)}")
        print(f"Chroma of signal 2 with it self: "
              f"{analysis.compare_two_chroma(audio_signal_2, audio_signal_2, sample_rate2, sample_rate2)}")
        print(f"Chroma between signals 1 and 2: "
              f"{analysis.compare_two_chroma(audio_signal_1, audio_signal_2, sample_rate1, sample_rate2)}")
        print(f"Chroma between signals 2 and 1: "
              f"{analysis.compare_two_chroma(audio_signal_2, audio_signal_1, sample_rate2, sample_rate1)}\n")

        print("Energy envelope comparison:")
        print(f"Energy envelope of signal 1 with it self: "
              f"{analysis.compare_two_energy_envelope(audio_signal_1, audio_signal_1)}")
        print(f"Energy envelope of signal 2 with it self: "
              f"{analysis.compare_two_energy_envelope(audio_signal_2, audio_signal_2)}")
        print(f"Energy envelope between signals 1 and 2: "
              f"{analysis.compare_two_energy_envelope(audio_signal_1, audio_signal_2)}")
        print(f"Energy envelope between signals 2 and 1: "
              f"{analysis.compare_two_energy_envelope(audio_signal_2, audio_signal_1)}\n")

        print("MFCC comparison:")
        print(f"MFCC of signal 1 with it self: "
              f"{analysis.compare_two_mfcc(audio_signal_1, audio_signal_1, sample_rate1, sample_rate1)}")
        print(f"MFCC of signal 2 with it self: "
              f"{analysis.compare_two_mfcc(audio_signal_2, audio_signal_2, sample_rate2, sample_rate2)}")
        print(f"MFCC between signals 1 and 2: "
              f"{analysis.compare_two_mfcc(audio_signal_1, audio_signal_2, sample_rate1, sample_rate2)}")
        print(f"MFCC between signals 2 and 1: "
              f"{analysis.compare_two_mfcc(audio_signal_2, audio_signal_1, sample_rate2, sample_rate1)}\n")

        print("Rhythm comparison:")
        print(f"Rhythm of signal 1 with itself: "
              f"{analysis.compare_two_rhythm(audio_signal_1, audio_signal_1, sample_rate1, sample_rate1)}")
        print(f"Rhythm of signal 2 with itself: "
              f"{analysis.compare_two_rhythm(audio_signal_2, audio_signal_2, sample_rate2, sample_rate2)}")
        print(f"Rhythm between signals 1 and 2: "
              f"{analysis.compare_two_rhythm(audio_signal_1, audio_signal_2, sample_rate1, sample_rate2)}")
        print(f"Rhythm between signals 2 and 1: "
              f"{analysis.compare_two_rhythm(audio_signal_2, audio_signal_1, sample_rate2, sample_rate1)}\n")

        print("Spectral contrast comparison:")
        print(f"Spectral contrast of signal 1 with it self: "
              f"{analysis.compare_two_spectral_contrast(audio_signal_1, audio_signal_1, sample_rate1, sample_rate1)}")
        print(f"Spectral contrast of signal 2 with it self: "
              f"{analysis.compare_two_spectral_contrast(audio_signal_2, audio_signal_2, sample_rate1, sample_rate1)}")
        print(f"Spectral contrast between signals 1 and 2: "
              f"{analysis.compare_two_spectral_contrast(audio_signal_1, audio_signal_2, sample_rate1, sample_rate1)}")
        print(f"Spectral contrast between signals 2 and 1: "
              f"{analysis.compare_two_spectral_contrast(audio_signal_2, audio_signal_1, sample_rate1, sample_rate1)}\n")

        print("Espectrograms comparison:")
        print(f"Espectrogram comparison of signal 1 with itself: "
              f"{analysis.compare_two_spectrograms(audio_signal_1, audio_signal_1)}")
        print(f"Espectrogram comparison of signal 2 with itself: "
              f"{analysis.compare_two_spectrograms(audio_signal_2, audio_signal_2)}")
        print(f"Espectrogram comparison between signals 1 and 2: "
              f"{analysis.compare_two_spectrograms(audio_signal_1, audio_signal_2)}")
        print(f"Espectrogram comparison between signals 2 and 1: "
              f"{analysis.compare_two_spectrograms(audio_signal_2, audio_signal_1)}\n")

        print("Zero Crossing Rate:")
        print(f"ZCR of signal 1 with itself: {analysis.compare_zcr(audio_signal_1, audio_signal_1)}")
        print(f"ZCR of signal 2 with itself: {analysis.compare_zcr(audio_signal_2, audio_signal_2)}")
        print(f"ZCR between signals 1 and 2: {analysis.compare_zcr(audio_signal_1, audio_signal_2)}")
        print(f"ZCR between signals 2 and 1: {analysis.compare_zcr(audio_signal_2, audio_signal_1)}\n")
    else:
        logging.critical("Could not access configuration file, suite execution aborted. The\n"
                         "configurations.json file should be located in the /core/artc_configurations/\n"
                         "folder. Check the directory and access permissions.")


if __name__ == "__main__":
    main()
