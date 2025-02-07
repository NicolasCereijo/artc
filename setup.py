import sys
from setuptools import setup, find_packages

# Check Python version
if sys.version_info < (3, 10) or sys.version_info >= (3, 13):
    sys.exit("Python 3.10 or higher and below 3.13 is required for this project.")


# Dependencies list
with open('requirements.txt') as f:
    requires = f.read().splitlines()

setup(
    name="artc",
    version="1.0b4",
    description="Beta version of the ARtC (Audio Real-time Comparator) core",
    long_description="A tool designed to compare and analyze audio files in real time.",
    author="Nicolás Cereijo Ranchal",
    author_email="nicolascereijoranchal@gmail.com",
    url="https://github.com/NicolasCereijo/artc",
    keywords=["audio", "analysis", "comparison", "real-time", "data collection"],
    license="MIT",
    install_requires=requires,
    packages=find_packages(),
    package_data={'core.configurations': ['default_configurations.json'],
                  'cli': ['commands.json']}
)
