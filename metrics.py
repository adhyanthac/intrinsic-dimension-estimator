import numpy as np
from sklearn.neighbors import NearestNeighbors


def compute_local_covariance(X, k=15):
    """
    Computes local covariance eigenvalues for each point using k-nearest neighbors.

    For each point x_i:
      1. Find its k nearest neighbors.
      2. Center the neighborhood (subtract mean).
      3. Compute the covariance matrix C_i of the centered neighbors.
      4. Compute eigenvalues of C_i, sorted descending.

    Parameters:
    - X: (n_points, dim) data array.
    - k: Number of nearest neighbors.

    Returns:
    - eigenvalues: (n_points, dim) array — each row holds sorted eigenvalues
      (largest first) for one point's local neighborhood.
    """
    n_points, dim = X.shape

    nbrs = NearestNeighbors(n_neighbors=k, algorithm='auto').fit(X)
    _, indices = nbrs.kneighbors(X)

    all_eigenvalues = []

    for i in range(n_points):
        neighbors = X[indices[i]]
        centered = neighbors - np.mean(neighbors, axis=0)

        # Covariance matrix (features × features)
        C_i = np.cov(centered.T)

        # Eigenvalues of symmetric matrix, sorted ascending → reverse to descending
        eigenvalues, _ = np.linalg.eigh(C_i)
        eigenvalues = eigenvalues[::-1]

        all_eigenvalues.append(eigenvalues)

    return np.array(all_eigenvalues)
