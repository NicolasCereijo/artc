import numpy as np


def adjust_length(*ndarrays: np.ndarray[float, ...]):
    """
        Adjusts the length of input ndarrays to be equal by truncating them to the minimum length.

        Args:
            *ndarrays (np.ndarray[float, ...]): NumPy arrays to be adjusted.

        Returns:
            adjusted_tuple (np.ndarray[float, ...]): Adjusted NumPy arrays with equal lengths.
    """
    min_length = min(map(lambda lst: len(lst), ndarrays))
    adjusted_ndarrays = tuple(np.array(ndarr[:min_length], dtype=np.float32) for ndarr in ndarrays)

    return adjusted_ndarrays


def adjust_dimensions(*ndarrays: np.ndarray[float, ...]):
    """
        Adjusts the dimensions of multiple NumPy arrays to have the same number of frames.

        Args:
            *ndarrays (Tuple[np.ndarray[float, ...]]): Variable number of NumPy arrays.

        Returns:
            List[np.ndarray[float, ...]]: List of adjusted NumPy arrays with the same number of frames.
    """
    min_frames = min(array.shape[1] for array in ndarrays)
    return [array[:, :min_frames] for array in ndarrays]


def normalize_btw_0_1(*ndarrays: tuple[np.ndarray[float, ...], ...]):
    """
        Normalize the input ndarrays between 0 and 1.

        Args:
            *ndarrays (tuple[np.ndarray[float, ...], ...]): Tuple with the NumPy arrays to be normalized.

        Returns:
            normalized_ndarrays (tuple): A tuple of normalized NumPy arrays between 0 and 1.
    """
    min_val = min(min(np.ravel(lst)) for lst in ndarrays[0])
    max_val = max(max(np.ravel(lst)) for lst in ndarrays[0])

    normalized_ndarrays = tuple(map(lambda lst: list(
        map(lambda x: (x - min_val) / (max_val - min_val), lst)), ndarrays))

    return normalized_ndarrays
