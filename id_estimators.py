import numpy as np


def estimate_spectral_gap_id(eigenvalues):
    """
    Estimates intrinsic dimension using the spectral gap method.

    For each point, the eigenvalues of its local covariance are sorted
    descending (lambda_0 >= lambda_1 >= ... >= lambda_{d-1}).

    The "gap" between consecutive eigenvalues is:
        gap_j = lambda_j - lambda_{j+1}

    The largest gap separates the "signal" eigenvalues (tangent space
    directions) from the "noise" eigenvalues (normal space / noise).
    The index of the largest gap + 1 gives the estimated intrinsic dimension.

    Parameters:
    - eigenvalues: (n_points, dim) array of sorted eigenvalues (descending).

    Returns:
    - global_id: Median intrinsic dimension estimate across all points.
    - local_ids: (n_points,) array of per-point ID estimates.
    """
    n_points = eigenvalues.shape[0]
    local_ids = []

    for i in range(n_points):
        evals = eigenvalues[i]
        gaps = evals[:-1] - evals[1:]  # descending, so gaps are positive

        if len(gaps) == 0:
            local_ids.append(0)
            continue

        largest_gap_idx = np.argmax(gaps)
        local_ids.append(largest_gap_idx + 1)

    local_ids = np.array(local_ids)
    global_id = int(np.median(local_ids))

    return global_id, local_ids
