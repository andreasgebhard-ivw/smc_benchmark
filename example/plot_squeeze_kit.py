import pathlib as pl

import matplotlib.pyplot as plt

from smc_benchmark.read import kit

folder = pl.Path.cwd() / "data"


data = kit(folder)

# Plot all configurations
for material, configs in data.items():
    for config, experiments in configs.items():
        fig, ax = plt.subplots(1,1)
        for experiment in experiments:
            ax.plot(experiment["h"], experiment["F"])
        ax.set_xlabel("Gap in s")
        ax.set_ylabel("Force in N")
        ax.set_title(f"Force vs Gap for {material} {config}")
        plt.savefig(f"{material}_{config}.png")
        plt.close()
