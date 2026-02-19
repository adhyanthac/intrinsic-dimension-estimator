import numpy as np
import os

from sphere import generate_sphere, add_noise
from metrics import compute_local_covariance
from id_estimators import estimate_spectral_gap_id
import plots


def run_noise_experiment(output_dir="results"):
    """
    Core experiment: generate a sphere, sweep over noise levels,
    estimate intrinsic dimension at each level, and produce all plots.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # ----- Generate the clean sphere -----
    print("Generating sphere (2500 points, radius=1) ...")
    X_clean = generate_sphere(n_points=2500, radius=1.0, seed=42)

    # Plot clean sphere
    plots.plot_sphere_3d(
        X_clean,
        "Clean Sphere (σ = 0)",
        os.path.join(output_dir, "sphere_clean.png"),
    )

    # ----- Noise sweep -----
    sigmas = [0, 0.05, 0.1, 0.2, 0.5]

    results = {
        "sigma": [],
        "id_estimate": [],
        "spectra": {},  # sigma -> (mean_evals, std_evals)
    }

    for sigma in sigmas:
        print(f"\n--- σ = {sigma} ---")

        X_noisy = add_noise(X_clean, sigma=sigma, seed=42)

        # Plot noisy sphere for a few representative noise levels
        if sigma in [0.1, 0.5]:
            plots.plot_sphere_3d(
                X_noisy,
                f"Noisy Sphere (σ = {sigma})",
                os.path.join(output_dir, f"sphere_sigma_{sigma}.png"),
            )

        # Compute local covariance eigenvalues
        print("  Computing local covariance eigenvalues ...")
        eigenvalues = compute_local_covariance(X_noisy, k=15)

        # Per-point eigenvalue plot (like the reference images)
        plots.plot_eigenvalues_per_point(
            eigenvalues,
            f"Per-Point Eigenvalues  (σ = {sigma})",
            os.path.join(output_dir, f"eigenvalues_per_point_sigma_{sigma}.png"),
        )

        # Store mean/std for the grouped-bar spectra plot
        mean_ev = np.mean(eigenvalues, axis=0)
        std_ev = np.std(eigenvalues, axis=0)
        results["spectra"][sigma] = (mean_ev, std_ev)

        # Estimate intrinsic dimension
        global_id, local_ids = estimate_spectral_gap_id(eigenvalues)
        results["sigma"].append(sigma)
        results["id_estimate"].append(global_id)

        print(f"  Estimated ID (spectral gap) = {global_id}")

    # ----- Summary table -----
    print("\n" + "=" * 40)
    print("  σ       Estimated ID")
    print("-" * 40)
    for s, est in zip(results["sigma"], results["id_estimate"]):
        print(f"  {s:<8}{est}")
    print("=" * 40)

    # ----- Aggregate plots -----
    print("\nGenerating summary plots ...")

    plots.plot_eigenvalue_spectra_by_noise(
        results["spectra"],
        os.path.join(output_dir, "eigenvalue_spectra_by_noise.png"),
    )

    plots.plot_id_vs_noise(
        results["sigma"],
        results["id_estimate"],
        os.path.join(output_dir, "id_vs_noise.png"),
    )

    return results
