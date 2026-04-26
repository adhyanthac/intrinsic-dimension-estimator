# Intrinsic Dimension Estimator

This repository is a classical simulation baseline for intrinsic dimension (ID) estimation on point-cloud data. The current experiment uses a uniformly sampled 2-sphere embedded in `R^3`, adds controlled Gaussian noise, and estimates intrinsic dimension from local covariance spectra.

The project is intentionally small, but it already contains the full loop:

1. generate a manifold with known ground-truth dimension,
2. perturb it with noise,
3. build local neighborhoods,
4. compute covariance eigenvalues,
5. infer local and global intrinsic dimension from the spectral gap,
6. visualize where and why the method succeeds or fails.

It is best read as both a working experiment and a scaffold for more advanced estimators.

## Why intrinsic dimension matters

Many datasets live in a high-dimensional ambient space while actually varying along a much smaller set of latent degrees of freedom. A point cloud may have three coordinates, hundreds of features, or thousands of pixels, while the true geometry only depends on a handful of variables.

Intrinsic dimension asks:

`How many independent directions does the data really vary along?`

For the 2-sphere used here:

- the ambient dimension is `3`,
- the intrinsic dimension is `2`,
- the missing direction is the normal direction off the surface.

This makes the sphere a clean benchmark. We know the correct answer in advance, so the behavior of the estimator can be interpreted geometrically rather than guessed from black-box outputs.

## Theory behind the estimator

### 1. Local linearity of smooth manifolds

A smooth manifold looks curved globally but approximately flat in a small enough neighborhood. Around each point on a 2-sphere, the data locally resembles a 2-dimensional tangent plane.

That means:

- two directions should carry meaningful local variance,
- one direction should have near-zero variance in the noiseless case.

This is the geometric fact the estimator exploits.

### 2. Local covariance as a tangent-space probe

Given a point `x_i`, the code finds its `k` nearest neighbors and computes the covariance matrix of that local neighborhood:

```text
C_i = cov({x_j : x_j in N_k(x_i)})
```

If the neighborhood is small enough and the sampling is dense enough, the eigenvectors of `C_i` approximate principal local directions, while the eigenvalues measure how much variation appears along those directions.

For a clean sphere in `R^3`, we expect:

```text
lambda_0 > 0
lambda_1 > 0
lambda_2 ~ 0
```

where:

- `lambda_0` and `lambda_1` correspond to tangent directions on the surface,
- `lambda_2` corresponds roughly to the normal direction.

### 3. Spectral gap criterion

The eigenvalues are sorted in descending order. The estimator then computes consecutive gaps:

```text
gap_j = lambda_j - lambda_(j+1)
```

The largest drop is interpreted as the boundary between signal and noise. If the largest gap is between `lambda_1` and `lambda_2`, then there are two meaningful directions and the local intrinsic dimension is estimated as `2`.

This is exactly what `id_estimators.py` implements.

### 4. Why noise breaks the method

Additive Gaussian noise pushes points away from the manifold and inflates variance in all directions, especially the directions that were previously small. As the smallest eigenvalue rises, the spectral separation between tangent and normal directions becomes less distinct.

Once that gap blurs, the largest drop may move earlier in the spectrum, causing underestimation. In this repo, the noisy sphere often shifts from the correct estimate `2` down to `1` at larger noise levels.

That failure mode is not a bug. It is the point of the experiment.

## What the current pipeline does

The experiment is orchestrated by [main.py](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/main.py) and [experiments.py](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/experiments.py).

### Dataset generation

[sphere.py](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/sphere.py) creates `2500` points on the unit sphere by sampling Gaussian vectors in `R^3` and normalizing them. This produces a uniform distribution on the sphere surface.

Noise is then added with fixed standard deviations:

```text
sigma in {0, 0.05, 0.1, 0.2, 0.5}
```

The random seed is fixed to `42` for reproducibility.

### Local covariance calculation

[metrics.py](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/metrics.py) uses `sklearn.neighbors.NearestNeighbors` with `k = 15`.

For each point:

1. collect its nearest neighbors,
2. center the neighborhood,
3. compute the covariance matrix,
4. extract eigenvalues with `numpy.linalg.eigh`,
5. reverse the order so the spectrum is descending.

The output has shape `(n_points, ambient_dim)`, so in the current sphere experiment each point gets three eigenvalues.

### Intrinsic dimension estimation

[id_estimators.py](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/id_estimators.py) computes a local ID for every point by selecting the index of the largest consecutive eigenvalue gap and adding `1`.

Those per-point estimates are then aggregated with the median:

```text
global ID = median(local IDs)
```

The median is a practical robust summary because some neighborhoods may be atypical even when the overall manifold is simple.

### Visualization

[plots.py](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/plots.py) produces four kinds of diagnostics:

- 3D sphere scatter plots,
- per-point eigenvalue plots,
- grouped spectra across noise levels,
- ID-vs-noise summary curves.

These plots are not just presentation assets. They are the debugging surface for the estimator.

## Repository structure

| Path | Role |
| --- | --- |
| [main.py](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/main.py) | Entry point. Creates the output directory and launches the experiment. |
| [experiments.py](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/experiments.py) | Defines the end-to-end noise sweep and records summary statistics. |
| [sphere.py](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/sphere.py) | Generates the sphere and applies isotropic Gaussian noise. |
| [metrics.py](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/metrics.py) | Computes local covariance matrices and their eigenvalues. |
| [id_estimators.py](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/id_estimators.py) | Implements the spectral-gap intrinsic-dimension estimator. |
| [plots.py](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/plots.py) | Saves the diagnostic figures. |
| [requirements.txt](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/requirements.txt) | Minimal Python dependencies. |
| [results](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/results) | Output folder for generated figures. |

## How to run it

Create or activate a Python environment with the packages in [requirements.txt](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/requirements.txt), then run:

```bash
pip install -r requirements.txt
python main.py
```

The script writes figures to `results/`.

## How to read the outputs

### `sphere_clean.png`

This is the geometric ground truth. Every point lies on the sphere surface, so there should be no meaningful variance off the manifold.

### `sphere_sigma_0.1.png` and `sphere_sigma_0.5.png`

These show how the manifold becomes a noisy shell rather than a clean surface. The farther the points drift radially, the harder it is for local covariance to separate tangent and normal directions.

### `eigenvalues_per_point_sigma_*.png`

These are the most informative plots in the repository.

In the clean case:

- the first two eigenvalue bands stay visibly above zero,
- the third band remains near zero,
- the gap between the second and third eigenvalue is clear.

In the noisy case:

- the smallest eigenvalue rises,
- the bands overlap more,
- the spectral gap becomes ambiguous.

### `eigenvalue_spectra_by_noise.png`

This summarizes how the average spectrum changes with noise. It is the fastest way to see the mechanism of failure without scanning thousands of individual neighborhoods.

### `id_vs_noise.png`

This is the headline result. It compresses the entire experiment into one question:

`At what noise level does the classical spectral-gap estimator stop recovering the true dimension?`

## Expected behavior under the default sweep

Based on the current experiment configuration and the tracked result figures in `results/`, the qualitative behavior is:

- `sigma = 0`: the estimator correctly returns intrinsic dimension `2`,
- `sigma = 0.05`: the estimate remains stable at `2`,
- `sigma >= 0.1`: the estimate can collapse to `1` because the smallest eigenvalue is no longer clearly separated from the tangent spectrum.

That pattern is the main empirical takeaway of the repository in its present form.

## Current assumptions and limitations

The present implementation is intentionally simple. That makes it easy to understand, but it also means the conclusions should be interpreted with those simplifications in mind.

### Fixed manifold family

Only a single manifold is implemented: a 2-sphere in `R^3`. The estimator is therefore being tested on the friendliest possible geometry.

### Fixed neighborhood size

`k = 15` is hard-coded in the experiment. This matters because neighborhood size directly controls the bias-variance tradeoff:

- too small and covariance estimates are unstable,
- too large and local neighborhoods stop being local.

### Fixed estimator

The project currently uses one estimator only: largest spectral gap. There is no side-by-side comparison against alternative classical baselines.

### Fixed aggregation rule

Global ID is the median of local estimates. That is reasonable, but not the only choice. Mode, trimmed mean, confidence-weighted summaries, or full local-ID distributions may tell a richer story.

### No uncertainty quantification

The pipeline reports point estimates, not confidence intervals. It does not yet run repeated trials over different random seeds.

## Best ways to improve the project next

This is the part most worth acting on if you want to grow the repo from a compact baseline into a more serious research tool.

### 1. Generalize the manifolds in `sphere.py`

Add more benchmark geometries:

- circles in `R^2`,
- tori in `R^3`,
- Swiss rolls,
- products of manifolds,
- higher-dimensional spheres embedded in larger ambient spaces.

This would let the repo separate "works on a sphere" from "works across geometries."

### 2. Make neighborhoods adaptive in `metrics.py`

Right now the code uses a fixed `k`. Future variants could use:

- radius-based neighborhoods,
- locally adaptive `k`,
- density-aware neighborhoods,
- weighted covariance where nearer points contribute more.

This is one of the most promising knobs for improving robustness.

### 3. Add more estimators in `id_estimators.py`

A strong next step is to turn `id_estimators.py` into a small estimator library. Good additions include:

- thresholded eigenvalue counting,
- participation ratio / effective rank,
- Levina-Bickel MLE,
- TwoNN,
- local PCA variants with scale selection,
- bootstrap-stabilized spectral gap rules.

Once multiple estimators exist, the repo can compare robustness rather than report a single method in isolation.

### 4. Promote experiment settings into configuration

[experiments.py](/c:/Users/adhya/Desktop/ID_estimate_classical_sim/experiments.py) currently hard-codes:

- `n_points = 2500`,
- `radius = 1.0`,
- `sigmas = [0, 0.05, 0.1, 0.2, 0.5]`,
- `k = 15`,
- `seed = 42`.

These should eventually become function arguments, a config object, or command-line flags so larger sweeps can be run without editing source code.

### 5. Track repeated trials and uncertainty

Instead of one run per noise level, run many seeds and record:

- mean estimated ID,
- standard deviation,
- failure rate,
- local-ID histograms,
- confidence intervals.

That would turn the project from a single illustrative run into a more defensible empirical study.

### 6. Add tests

The codebase is small enough that a focused test suite would go a long way. Good first tests:

- sphere samples have unit norm before noise,
- zero-noise addition returns a copy with unchanged values,
- covariance spectra are sorted descending,
- clean-sphere ID is `2` under the default settings,
- degenerate or tiny inputs fail clearly.

### 7. Improve outputs for research reuse

Right now the project primarily writes plots. It would be useful to also save:

- raw eigenvalue arrays,
- per-point ID estimates,
- summary JSON or CSV files,
- experiment metadata such as `k`, `sigma`, seed, and sample count.

That would make it easier to compare runs and feed the outputs into notebooks or papers.

### 8. Prepare for the quantum comparison

Because the motivation of this repository is to establish a classical baseline, the next architectural step is to define a common experiment interface:

- same datasets,
- same noise models,
- same evaluation metrics,
- same plots,
- different estimators underneath.

That way the future quantum method can plug into the same pipeline and be compared fairly rather than anecdotally.

## Suggested refactor direction

If the repo keeps growing, the cleanest structural upgrade would be to separate:

- data generation,
- neighborhood construction,
- estimators,
- experiment configuration,
- plotting,
- persistence of outputs.

At that point, a package layout such as `manifolds/`, `estimators/`, `experiments/`, and `visualization/` would make sense. For the current scale, the flat layout is still perfectly readable.

## Bottom line

This repository demonstrates a clear and useful baseline:

- local covariance captures tangent-space structure on a clean manifold,
- the spectral gap recovers the correct intrinsic dimension in low noise,
- noise inflates the normal-direction eigenvalues and can erase the decisive gap,
- the resulting failure motivates more robust estimators.

That makes the project successful both as a computational experiment and as a launch point for deeper work.
