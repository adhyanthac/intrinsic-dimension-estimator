import os
import experiments


def main():
    print("=" * 55)
    print("  Intrinsic Dimension Estimation — Classical Simulation")
    print("=" * 55)
    print("Manifold  :  2-Sphere (S²) embedded in ℝ³")
    print("True ID   :  2")
    print("Method    :  Local Covariance → Spectral Gap")
    print("=" * 55)

    output_dir = "results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Results → {os.path.abspath(output_dir)}\n")

    experiments.run_noise_experiment(output_dir)

    print("\n" + "=" * 55)
    print("  Done.  Check the 'results/' folder for all plots.")
    print("=" * 55)


if __name__ == "__main__":
    main()
