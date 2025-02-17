import pathlib as pl

import numpy as np
import pandas as pd

from smc_benchmark._naming import KIT_NAMING
from smc_benchmark._utils import decode_filename

NUMBER_TO_DISTANCE = {1: "3mm", 4: "6mm", 9: "9mm"}
CONFIG_TO_NUMBER_KIT = {
    "3mm 100x100": [3, 7, 11, 15, 19, 23],
    "3mm 50x50": [4, 8, 12, 16, 20, 24],
    "5mm 100x100": [2, 6, 10, 14, 18, 22],
    "7mm 100x100": [1, 5, 9, 13, 17, 21],
}
NUMBER_TO_CONFIG_KIT = {v: k for k, values in CONFIG_TO_NUMBER_KIT.items() for v in values}


def kit(folder):
    """Read KIT test data."""
    folder = pl.Path(folder)
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder}")

    # Read data
    all_data = {}
    for file in folder.glob("*.txt", case_sensitive=False):
        _, material, number = decode_filename(file.stem)

        # Read individual experiment
        data = np.loadtxt(file, delimiter=",", encoding="latin1", skiprows=5).T
        pd_data = pd.DataFrame(data[list(KIT_NAMING.keys())].T, columns=list(KIT_NAMING.values()))

        # Add experiment to all data
        if material not in all_data:
            all_data[material] = {}
        specification = NUMBER_TO_CONFIG_KIT[int(number)]
        if specification not in all_data[material]:
            all_data[material][specification] = []
        all_data[material][specification].append(pd_data)

    # TODO : Manipulate data to match the desired format
    return all_data


def tum():
    pass
