# -*- coding: utf-8 -*-
"""
@author: Miro Duhovic, miro.duhovic@ivw.uni-kl.de
@author: Andreas Gebhard, andreas.gebhard@ivw.uni-kl.de
"""
# standard library imports
import os
from shutil import copy2

# local application imports
# none

# third party library imports
import pandas as pd


def sort_image_dir(*, excel, indir, outdir, institution):
    """
    Sorts images which are stored in an input directory.

    Parameters:
    -----------
    excel : str | Path
        The path to the Excel file containing the test plan of the institution.

    indir : str | Path
        The input directory where the images are located.

    outdir : str | Path
        The output directory where the sorted images will be saved.

    institution : str
        The name of the institution associated with the images being sorted.

    Returns:
    --------
    None
        This function does not return any value. It performs sorting and saves the result to the specified output directory.

    Notes:
    ------
    - The `indir` path should be a valid directory in the filesystem.
    - The `outdir` path gets created if it does not exist
    """

    # Loop through all sheets
    for sheet_name in ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5']:
        # Read the sheet into a DataFrame
        df = pd.read_excel(excel, sheet_name=sheet_name)

        # Get the number of rows in the current sheet
        num_rows = len(df)

        # Loop through rows 20 to 44 (inclusive), which are rows 19 to 43 in 0-based indexing
        # Make sure we don't go beyond the number of rows in the DataFrame
        for row in range(19, min(44, num_rows)):  # Ensures no out-of-bounds error
            material_name = df.iloc[row, 3]  # get material name from column D (index 3 in pandas)
            specimen_size = df.iloc[row, 4]  # get specimen size from column E (index 4 in pandas)
            specimen_thickness = df.iloc[row, 9]  # get specimen thickness from column J (index 9 in pandas)
            specimen_thickness_with_mm = f"{specimen_thickness}mm"  # Append 'mm' to the specimen thickness
            # Create subfolder name by combining the institution with material name, specimen size, and thickness
            folder_name = f"{institution}-{material_name}_{specimen_size}_{specimen_thickness_with_mm}"

            image_file_name = df.iloc[row, 1]  # get image file name from column B (index 1 in pandas)
            # Add institution prefix to the image filename and append '_8bit.bmp'
            image_file_name = f"{institution}-{image_file_name.strip()}_8bit.bmp"

            # Construct the folder path for the new folder
            # created from institution, material name, size and thickness
            folder_path = os.path.join(outdir, folder_name)

            # Create the folder if it doesn't exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Construct the full source file path (with the name from column B)
            source_file_path = os.path.join(indir, image_file_name)

            # Construct the destination file path (keeping the original filename)
            destination_file_path = os.path.join(folder_path, image_file_name)

            # Copy the image to the corresponding folder with the original name (including _8bit.bmp)
            try:
                copy2(source_file_path, destination_file_path)
                print(f"Image '{image_file_name}' copied to '{folder_path}'")
            except FileNotFoundError:
                print(f"File '{source_file_path}' not found, skipping.")
            except Exception as e:
                print(f"Error processing file {source_file_path}: {e}")

    print("Process completed.")
