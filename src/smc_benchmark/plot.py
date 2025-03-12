"""Plot all squeeze experiments of an institution."""
import os
import pathlib as pl
import matplotlib.pyplot as plt
from smc_benchmark.read import read


def plot_gap_force(*, institution, indir, outdir=None, dpi=300):

    # Folder with experimental data
    indir = pl.Path(indir)

    # Set outdir for plots
    if outdir is None:
        outdir = indir
    else:
        outdir = pl.Path(outdir)

    # Read experimental data
    data = read(institution, indir)

    # Plot all configurations
    for material, configs in data.items():
        for config, experiments in configs.items():
            fig, ax = plt.subplots(1, 1)
            for experiment in experiments:
                ax.plot(experiment["h"], experiment["F"])
            ax.set_xlabel("Gap in mm")
            ax.set_ylabel("Force in N")
            ax.set_title(f"{material} {config}")
            fig_path = outdir / f"{material}_{config}.png"
            plt.savefig(fig_path, dpi=dpi)
            plt.close()
