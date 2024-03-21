from typing import Iterable
import numpy as np


def adjust_length(*ndarrays: np.ndarray[float, ...]) -> tuple[np.ndarray[..., np.dtype], ...]:
    min_length = min(map(lambda lst: len(lst), ndarrays))
    adjusted_ndarrays = tuple(np.array(ndarr[:min_length], dtype=np.float32) for ndarr in ndarrays)

    return adjusted_ndarrays


def adjust_dimensions(*ndarrays: np.ndarray[float, ...]) -> list[np.ndarray[float, ...]]:
    min_frames = min(array.shape[1] for array in ndarrays)
    return [array[:, :min_frames] for array in ndarrays]


def normalize_btw_0_1(*iterables: Iterable) -> tuple[list, ...]:
    min_val = min(min(np.ravel(itr)) for itr in iterables[0])
    max_val = max(max(np.ravel(itr)) for itr in iterables[0])

    normalized_ndarrays = tuple(map(lambda lst: list(
        map(lambda x: (x - min_val) / (max_val - min_val), lst)), iterables))

    return normalized_ndarrays
