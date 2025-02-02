import os
import multiprocessing
from pathlib import Path
from functools import partial

from core import analysis
import core.configurations as config
from core.datastructures import WorkingSet


def comparator(comparison):
    return comparison() * 100


def available_cores(configuration_path: Path) -> int:
    cpu_usage = config.read_config("cpu", configuration_path)
    cpu_cores = os.cpu_count()

    if not isinstance(cpu_usage, int) or not isinstance(cpu_cores, int):
        return 0
    return int(cpu_cores * (cpu_usage / 100))


def compare(metric: str, wset: WorkingSet, configuration_path: Path, set_to_use: str = "individual_files"):
    operations = []
    set = wset.working_set[set_to_use]
    cores = available_cores(configuration_path)

    if metric not in analysis.COMPARE_FUNCTIONS:
        raise ValueError(f"Metric {metric} invalid, available metrics are the following:\n{
            list(analysis.COMPARE_FUNCTIONS.keys())}")
    elif cores == 0:
        raise ValueError("Cannot calculate or access to system cores")

    for audio_1 in set:
        for audio_2 in range(len(set)):
            compare_func = analysis.COMPARE_FUNCTIONS[metric]["compare_two"]

            parameters = (
                compare_func,
                audio_1.audio_signal_unloaded(),
                set[audio_2].audio_signal_unloaded()
            )
            if analysis.COMPARE_FUNCTIONS[metric]["use_sample_rate"] is True:
                parameters += (
                    audio_1.sample_rate,
                    set[audio_2].sample_rate
                )

            operations.append(partial(*parameters))

    with multiprocessing.Pool(processes=cores) as pool:
            results = pool.map(comparator, operations)

    return results
