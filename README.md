# Classical Intrinsic Dimension Estimator

A classical simulation pipeline for estimating the **intrinsic dimension (ID)** of point-cloud data on a known manifold (2-sphere), using local covariance eigenvalue analysis. This serves as a **classical baseline** before exploring quantum-enhanced ID estimation methods.

## Context

This project is part of early-stage research preparation for a summer position at **Argonne National Laboratory**. The goal is to:

1. Build intuition for intrinsic dimension estimation on a controlled test case.
2. Understand how noise degrades ID estimates.
3. Establish classical baselines before moving to the quantum ML approach described in *"Robust Estimation of Intrinsic Dimension using Quantum Machine Learning"*.

## What Is Intrinsic Dimension?

A dataset may live in high-dimensional space (e.g. 100 features), but the data might actually only vary along a few directions — like points on the surface of a sphere in 3D only need 2 coordinates (latitude, longitude).

**Intrinsic dimension = the true number of independent directions the data varies along.**

For a 2-sphere (S²), the true ID is exactly **2**.

## How the Algorithm Works

For each point in the dataset:

1. **Find neighbors** — locate its 15 nearest neighbors.
2. **Local covariance** — compute the covariance matrix of that small neighborhood.
3. **Eigenvalues** — decompose the covariance into eigenvalues (λ₀ ≥ λ₁ ≥ λ₂).
   - Large eigenvalues = real directions on the manifold surface.
   - Small eigenvalues = noise / normal direction.
4. **Spectral gap** — the biggest drop between consecutive eigenvalues tells us where "signal" ends and "noise" begins. That cutoff index = estimated ID.

## Output Plots

| Plot | What It Shows |
|------|---------------|
| `sphere_clean.png` | 3D scatter of clean sphere (ground truth) |
| `sphere_sigma_*.png` | Sphere with Gaussian noise added |
| `eigenvalues_per_point_sigma_*.png` | Per-point eigenvalue breakdown — the key diagnostic |
| `eigenvalue_spectra_by_noise.png` | Summary: how noise lifts eigenvalues and erases the spectral gap |
| `id_vs_noise.png` | Bottom-line result: estimated ID vs noise level |

## File Structure

```
├── main.py             # Entry point
├── sphere.py           # Sphere generation + noise
├── metrics.py          # Local covariance eigenvalue computation
├── id_estimators.py    # Spectral gap ID estimation
├── experiments.py      # Noise sweep experiment orchestration
├── plots.py            # All visualization code
├── requirements.txt    # Dependencies
└── results/            # Generated plots
```

## Quick Start

```bash
pip install -r requirements.txt
python main.py
# → check results/ folder for all plots
```

## Key Findings (Week 1)

- **Clean sphere (σ=0):** Algorithm correctly estimates ID = **2**. The per-point eigenvalue plot shows two nonzero eigenvalue bands (e0, e1) and one flat-zero band (e2), confirming the 2D tangent plane.
- **Low noise (σ ≤ 0.05):** ID estimate remains robust at **2**.
- **High noise (σ ≥ 0.1):** Estimate degrades to **1** — noise inflates e2, blurring the spectral gap. This motivates exploration of more robust (potentially quantum) methods.

## Next Steps

- Compare with quantum kernel–based ID estimation from the reference paper.
- Test on higher-dimensional manifolds and non-trivial topologies.
- Explore adaptive neighborhood size (k) to improve noise robustness.
