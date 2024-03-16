import numpy as np


def adjust_length(*ndarrays: np.ndarray[float, ...]):
    """
        Adjusts the length of input ndarrays to be equal by truncating them to the minimum length.

        Args:
            *ndarrays (np.ndarray[float, ...]): Numpy arrays to be adjusted.

        Returns:
            adjusted_tuple (np.ndarray[float, ...]): Adjusted Numpy arrays with equal lengths.
    """
    min_length = min(map(lambda lst: len(lst), ndarrays))
    adjusted_ndarrays = tuple(np.array(ndarr[:min_length], dtype=np.float32) for ndarr in ndarrays)

    return adjusted_ndarrays


def normalize_btw_0_1(*ndarrays: tuple[np.ndarray[float, ...], ...]):
    """
        Normalize the input ndarrays between 0 and 1.

        Args:
            *ndarrays (tuple[np.ndarray[float, ...], ...]): Tuple with the Numpy arrays to be normalized.

        Returns:
            normalized_ndarrays (tuple): A tuple of normalized Numpy arrays between 0 and 1.
    """
    min_val = min(min(np.ravel(lst)) for lst in ndarrays[0])
    max_val = max(max(np.ravel(lst)) for lst in ndarrays[0])

    normalized_ndarrays = tuple(map(lambda lst: list(
        map(lambda x: (x - min_val) / (max_val - min_val), lst)), ndarrays))

    return normalized_ndarrays
