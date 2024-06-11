import numpy as np


def adjust_length(*ndarrays: np.ndarray[float, ...]) -> tuple[np.ndarray[..., np.dtype], ...]:
    min_length = min(map(lambda lst: len(lst), ndarrays))
    adjusted_ndarrays = tuple(np.array(ndarr[:min_length], dtype=np.float32) for ndarr in ndarrays)

    return adjusted_ndarrays


def adjust_dimensions(*ndarrays: np.ndarray[float, ...]) -> list[np.ndarray[float, ...]]:
    min_frames = min(array.size for array in ndarrays)
    return [array[:min_frames] for array in ndarrays]


def normalize_btw_0_1(*iterables: np.ndarray[float, ...]) -> tuple[list, ...]:
    all_values = np.hstack(iterables)
    min_val = np.min(all_values)
    max_val = np.max(all_values)

    normalized_ndarrays = tuple(map(lambda lst: list(
        map(lambda x: (x - min_val) / (max_val - min_val), lst)), iterables))

    return normalized_ndarrays
