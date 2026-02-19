# Talking Points — Weekly Update (Feb 19, 2026)
# Target: ~15 minutes with PI

## Slide / Section 1 — What I Did This Week (2 min)
- "I built a classical baseline for intrinsic dimension estimation."
- "I'm using a 2-sphere (S²) as the test manifold — true ID is exactly 2."
- "The method is local covariance eigenvalue analysis with a spectral gap criterion."
- "I swept across 5 noise levels (σ = 0 to 0.5) to test robustness."

## Slide / Section 2 — Show the Clean Sphere Eigenvalue Plot (3 min)
- Pull up: `eigenvalues_per_point_sigma_0.png`
- "Each dot is one of 2500 points on the sphere."
- "For every point, I compute a local covariance matrix from its 15 nearest neighbors
   and extract the 3 eigenvalues."
- "Blue band (e0) and red band (e1) are both nonzero — these are the two tangent
   directions on the sphere surface."
- "Green band (e2) is flat at zero — there's no variance in the radial direction
   because all points sit exactly on the sphere."
- "Two nonzero eigenvalues + one zero → spectral gap between e1 and e2 → ID = 2. ✓"

## Slide / Section 3 — Show the Noisy Sphere (3 min)
- Pull up: `eigenvalues_per_point_sigma_0.5.png` side by side with σ=0
- "Now I add Gaussian noise (σ=0.5). The points scatter off the surface."
- "All three eigenvalue bands rise and start overlapping."
- "The gap between e1 and e2 is no longer clear — noise has inflated
   the radial direction."
- "The algorithm now underestimates: it reports ID=1 instead of 2."

## Slide / Section 4 — Summary Bar Chart (2 min)
- Pull up: `eigenvalue_spectra_by_noise.png`
- "This condenses everything. Each group is one eigenvalue component.
   Bar color = noise level."
- "For σ=0 (dark blue), e2 is nearly zero — clear gap."
- "For σ=0.5 (red), e2 has grown substantially — the gap is gone."

## Slide / Section 5 — The Bottom Line (2 min)
- Pull up: `id_vs_noise.png`
- "At low noise (σ ≤ 0.05), the classical method correctly gets ID=2."
- "At σ ≥ 0.1, it drops to 1. The spectral gap method is accurate but
   not infinitely robust."
- "This motivates exploring quantum kernel methods that may preserve
   the spectral gap under noise — which is exactly what the paper proposes."

## Slide / Section 6 — Next Steps (2 min)
- "Next week I plan to:
  1. Read through the quantum kernel ID estimation method from the paper.
  2. Compare what changes: the key claim is that quantum feature maps
     can separate signal eigenvalues from noise eigenvalues more robustly.
  3. Potentially test on a higher-dimensional manifold (e.g., a torus
     or a product manifold) to see if the classical method degrades
     further as true ID increases."

## If PI Asks Questions — Prepared Answers:
- "Why a sphere and not a torus?"
  → "A sphere is the simplest 2D manifold — fewer parameters, clearer
     results. The torus introduces curvature variations that complicate
     interpretation for a first pass."

- "Why does high noise cause ID=1 instead of ID=3?"
  → "Noise inflates ALL eigenvalues, but not equally. It tends to make
     the largest eigenvalue dominate even more (because noise adds
     variance in all directions, and the already-large direction gets
     the biggest absolute boost). So the biggest gap shifts from
     'between e1 and e2' to 'between e0 and e1'."

- "How does this connect to the quantum paper?"
  → "The paper proposes using a quantum kernel to map data into a
     Hilbert space where the spectral gap is amplified. Classical
     covariance is limited by the ambient geometry — quantum feature
     maps can potentially reshape the spectrum to make the gap more
     robust to noise."

- "What is the spectral gap exactly?"
  → "It's just the biggest jump between consecutive eigenvalues when
     sorted from largest to smallest. If eigenvalues are [10, 8, 0.1],
     the gap is between 8 and 0.1 — that tells us there are 2 'real'
     directions and the rest is noise."
