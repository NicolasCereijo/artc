import gc
import os
import multiprocessing
import psutil
import resource
from functools import partial
from pathlib import Path

import numpy as np

from core import analysis
from core import errors
import core.configurations as config
from core.datastructures import WorkingSet


logger = errors.logger_config.LoggerSingleton().get_logger()


def comparator(comparison):
    try:
        return comparison() * 100
    except MemoryError:
        logger.warning("An operation was aborted due to insufficient memory")
        return -1


def available_processes(configuration_path: Path) -> int:
    processes = config.read_config("processes", configuration_path)
    cpu_cores = os.cpu_count()

    if not (isinstance(processes, int) and isinstance(cpu_cores, int) and processes <= cpu_cores):
        raise ValueError(
            "Available processes cannot be queried, or selected amount exceeds safety limit")
    return processes


def available_memory(configuration_path: Path) -> int:
    mem_limit = config.read_config("memory", configuration_path)
    total_memory = psutil.virtual_memory().total

    if not isinstance(mem_limit, int) or not mem_limit <= 80:
        raise ValueError(
            "System's available memory cannot be queried, or selected amount exceeds safety limit")
    return int(total_memory * (mem_limit / 100))


def set_memory_limit(configuration_path: Path):
    memory = available_memory(configuration_path)

    try:
        resource.setrlimit(resource.RLIMIT_AS, (memory, resource.RLIM_INFINITY))
    except Exception:
        raise RuntimeError("The memory configuration is not compatible with the operating system")


def build_symmetric_matrix(values: list) -> np.ndarray:
    matrix_size = int((-1 + (1 + 8 * len(values)) ** 0.5) / 2)
    matrix = np.zeros((matrix_size, matrix_size))

    idx = 0
    for i in range(matrix_size):
        for j in range(i, matrix_size):
            matrix[i][j] = values[idx]
            if i != j:
                matrix[j][i] = values[idx]
            idx += 1
    return matrix


def compare(metric: str, wset: WorkingSet, configuration_path: Path,
    set_to_use: str = "individual_files") -> np.ndarray:
    set = wset.working_set[set_to_use]
    operations = []

    if metric not in analysis.COMPARE_FUNCTIONS:
        raise ValueError(f"Metric {metric} invalid, available metrics are the following:\n{
            list(analysis.COMPARE_FUNCTIONS.keys())}")

    for i in range(len(set)):
        for j in range(len(set) - i):
            compare_func = analysis.COMPARE_FUNCTIONS[metric]["compare_two"]

            parameters = (
                compare_func,
                set[i].audio_signal_unloaded(),
                set[i+j].audio_signal_unloaded()
            )
            if analysis.COMPARE_FUNCTIONS[metric]["use_sample_rate"] is True:
                parameters += (
                    set[i].sample_rate,
                    set[i+j].sample_rate
                )

            operations.append(partial(*parameters))

    set_memory_limit(configuration_path)

    with multiprocessing.Pool(processes=available_processes(configuration_path)) as pool:
        results = pool.map(comparator, operations)
    gc.collect()

    return build_symmetric_matrix(results)
