import sys
from setuptools import setup

# Check Python version
if sys.version_info < (3, 10):
    sys.exit("Python 3.10 or higher is required for this project.")

# Dependencies list
requires = [
        "colorlog==6.8.2",
        "librosa==0.10.1",
        "numpy==1.26.1",
        "pytest==8.0.1",
        "requests==2.31.0",
        "scikit-learn==1.3.2",
]

setup(
    name="artc-suite",
    version="1.0a2",
    description="Alpha version of the ARtC (Audio Real-time Comparator) core",
    long_description="A suite designed to compare and analyze audio files in real time.",
    author="Nicolás Cereijo Ranchal",
    author_email="nicolascereijoranchal@gmail.com",
    url="https://github.com/NicolasCereijo/artc-suite",
    keywords=["audio", "analysis", "comparison", "real-time", "data collection"],
    license="MIT",
    install_requires=requires,
)
