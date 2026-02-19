import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# ---------------------------------------------------------------------------
# 1.  3D Sphere Scatter
# ---------------------------------------------------------------------------
def plot_sphere_3d(X, title, filename):
    """
    Plots a 3D scatter of sphere points, colored by the z-coordinate
    so the viewer can see the shape clearly.
    """
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(
        X[:, 0], X[:, 1], X[:, 2],
        c=X[:, 2], cmap='viridis', s=4, alpha=0.7,
    )
    plt.colorbar(scatter, ax=ax, label='z-coordinate', shrink=0.6)
    ax.set_title(title, fontsize=13)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()


# ---------------------------------------------------------------------------
# 2.  Per-point eigenvalue plot  (matches the reference images)
# ---------------------------------------------------------------------------
def plot_eigenvalues_per_point(eigenvalues, title, filename):
    """
    Plots every eigenvalue component (e0, e1, e2) as a function of
    point index.  This is the style shown in the user's reference images.

    X-axis  = point index  (each of the N sampled points, in arbitrary order)
    Y-axis  = eigenvalue magnitude

    Each colored band represents one eigenvalue component:
      e0 (largest)  — if this is big, there is variance in that direction.
      e1 (second)   — same interpretation.
      e2 (smallest) — on a clean sphere this should be ~0.
    """
    n_points, dim = eigenvalues.shape
    xs = np.arange(n_points)

    fig, ax = plt.subplots(figsize=(10, 5))

    colors = ['#4363d8', '#e6194B', '#3cb44b']  # blue, red, green
    labels = [f'e{j}  (eigenvalue {j})' for j in range(dim)]

    # Plot from last to first so the largest (e0) is drawn on top
    for j in reversed(range(dim)):
        ax.scatter(xs, eigenvalues[:, j], s=1, alpha=0.5,
                   color=colors[j % len(colors)], label=labels[j])

    ax.set_xlabel('Point index', fontsize=11)
    ax.set_ylabel('Eigenvalue magnitude', fontsize=11)
    ax.set_title(title, fontsize=13)
    ax.legend(markerscale=6, fontsize=9)
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()


# ---------------------------------------------------------------------------
# 3.  Eigenvalue spectra across noise levels  (improved color-coding)
# ---------------------------------------------------------------------------
def plot_eigenvalue_spectra_by_noise(spectrum_data, filename):
    """
    For each noise level σ, plots the *mean* eigenvalue spectrum
    (mean across all points) as a bar group, color-coded by σ.

    X-axis groups = eigenvalue component (e0, e1, e2)
    Y-axis        = mean eigenvalue magnitude
    Color          = noise level σ
    Error bars    = ± 1 std across points.

    This clearly shows how noise "lifts" the small eigenvalues and
    blurs the spectral gap.
    """
    sigmas = sorted(spectrum_data.keys())
    n_components = None
    for s in sigmas:
        n_components = len(spectrum_data[s][0])
        break

    # Use a diverging colormap so clean=cool, noisy=warm
    cmap = plt.cm.coolwarm
    norm = plt.Normalize(vmin=min(sigmas), vmax=max(sigmas))

    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.8 / len(sigmas)
    x_base = np.arange(n_components)

    for i, sigma in enumerate(sigmas):
        mean_ev, std_ev = spectrum_data[sigma]
        offset = (i - len(sigmas) / 2) * bar_width + bar_width / 2
        color = cmap(norm(sigma))
        ax.bar(x_base + offset, mean_ev, width=bar_width,
               yerr=std_ev, capsize=3, color=color,
               label=f'σ = {sigma}', edgecolor='white', linewidth=0.5)

    ax.set_xlabel('Eigenvalue component (e0 = largest, e2 = smallest)', fontsize=11)
    ax.set_ylabel('Mean eigenvalue magnitude', fontsize=11)
    ax.set_title('Eigenvalue Spectra Across Noise Levels', fontsize=13)
    ax.set_xticks(x_base)
    ax.set_xticklabels([f'e{j}' for j in range(n_components)])
    ax.legend(title='Noise σ', fontsize=9)
    ax.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()


# ---------------------------------------------------------------------------
# 4.  ID vs Noise  (kept from before, slightly polished)
# ---------------------------------------------------------------------------
def plot_id_vs_noise(sigmas, estimated_ids, filename):
    """
    Plots the estimated intrinsic dimension as a function of noise σ.
    A horizontal dashed line marks the true ID = 2.
    """
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(sigmas, estimated_ids, 'o-', linewidth=2, markersize=8,
            color='#4363d8', label='Spectral Gap Estimate')
    ax.axhline(y=2, color='red', linestyle=':', linewidth=1.5,
               label='True ID = 2')

    ax.set_xlabel('Noise Standard Deviation (σ)', fontsize=11)
    ax.set_ylabel('Estimated Intrinsic Dimension', fontsize=11)
    ax.set_title('Intrinsic Dimension Estimate vs Noise Level', fontsize=13)
    ax.set_ylim(0, max(max(estimated_ids) + 1, 4))
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
