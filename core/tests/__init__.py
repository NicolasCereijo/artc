from core.tests import test_configurations, test_errors
import pytest
import os


def main():
    print("=================== Running the main test suite for ARtC... ====================")

    if os.access("../artc_configurations/configurations.json", os.R_OK):
        result = pytest.main()

        if result == 0:
            print("========================== All tests ran successfully ==========================")
        else:
            print("=============== Bugs were found in the test set during execution ===============")
    else:
        print("======= Could not access configuration file, tests execution was aborted =======")


if __name__ == "__main__":
    main()
