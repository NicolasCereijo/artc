from core.configurations import read_config
from pydub.utils import mediainfo
import os


def check_audio_format(file_path):
    file_extension = os.path.splitext(file_path)[1][1:].lower()
    if file_extension not in read_config("extensions"):
        ValueError("Invalid file format")


def check_audio_corruption(file_path):
    try:
        mediainfo(file_path)
    except Exception as ex:
        print(f"Audio file '{file_path}' is corrupted: {ex}")
