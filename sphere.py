import numpy as np


def generate_sphere(n_points=2500, radius=1.0, seed=42):
    """
    Generates uniformly distributed points on the surface of a 2-sphere (S^2).

    The surface of a sphere is a 2-dimensional manifold embedded in 3D space,
    so the true intrinsic dimension is exactly 2.

    Parameters:
    - n_points: Number of points to generate.
    - radius: Radius of the sphere.
    - seed: Random seed for reproducibility.

    Returns:
    - X: (n_points, 3) array of (x, y, z) coordinates on the sphere surface.
    """
    np.random.seed(seed)

    # Use the standard method for uniform sampling on a sphere:
    # Generate 3D Gaussian vectors and normalize them to unit length.
    # This gives a perfectly uniform distribution on S^2.
    raw = np.random.randn(n_points, 3)
    norms = np.linalg.norm(raw, axis=1, keepdims=True)
    X = radius * raw / norms

    return X


def add_noise(X, sigma=0.0, seed=42):
    """
    Adds isotropic Gaussian noise to the dataset.

    Parameters:
    - X: (n_points, dim) array of data points.
    - sigma: Standard deviation of Gaussian noise.
    - seed: Random seed for reproducibility.

    Returns:
    - X_noisy: (n_points, dim) array of noisy data points.
    """
    if sigma <= 0:
        return X.copy()

    np.random.seed(seed)
    noise = np.random.normal(0, sigma, X.shape)
    return X + noise
