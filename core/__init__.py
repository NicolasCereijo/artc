import core.artc_errors.validations.path as path_err


def main():
    print("Harvesting potatoes, stay tuned")
    path_err.validate_path("/home/nico/Música/Investigación/Colección sonidos investigación/Sonidos de agua/",
                           "Air Woosh Underwater.mp3")
    path_err.validate_path("https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/",
                           "bootstrap.min.css")


if __name__ == "__main__":
    main()
