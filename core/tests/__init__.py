from core.tests import test_configurations, test_errors
import pytest


def main():
    print("=================== Running the main test suite for ARtC... ====================")

    result = pytest.main()

    if result == 0:
        print("========================== All tests ran successfully ==========================")
    else:
        print("=============== Bugs were found in the test set during execution ===============")


if __name__ == "__main__":
    main()
