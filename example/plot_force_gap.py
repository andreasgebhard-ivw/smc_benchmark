"""Plot all squeeze experiments of an institution."""

import pathlib as pl

import matplotlib.pyplot as plt

from smc_benchmark.read import read_kit  # change to read function of interest

# Folder with experimental data
folder = pl.Path(r"path/to/folder")

# Read experimental data
data = read_kit(folder)

# Plot all configurations
for material, configs in data.items():
    for config, experiments in configs.items():
        fig, ax = plt.subplots(1, 1)
        for experiment in experiments:
            ax.plot(experiment["h"], experiment["F"])
        ax.set_xlabel("Gap in s")
        ax.set_ylabel("Force in N")
        ax.set_title(f"{material} {config}")
        plt.savefig(f"{material}_{config}.png", dpi=300)
        plt.close()
