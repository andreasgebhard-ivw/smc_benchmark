# -*- coding: utf-8 -*-
"""
@author: Miro Duhovic, miro.duhovic@ivw.uni-kl.de
@author: Andreas Gebhard, andreas.gebhard@ivw.uni-kl.de
"""

import cv2
import logging
import numpy as np
import os
import torch
from segment_anything import sam_model_registry, SamPredictor, SamAutomaticMaskGenerator
from pathlib import Path

# Allow multiple instances of the Intel OpenMP (KMP) runtime
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Construct the path to the SAM model file ...
model_path = Path(__file__).parent.parent / 'resources' / 'sam' / 'sam_vit_h_4b8939.pth'
# ... and load the SAM model
sam = sam_model_registry["vit_h"](checkpoint=model_path)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
sam.to(device)
predictor = SamPredictor(sam)
mask_generator = SamAutomaticMaskGenerator(sam)


def setup_logging(log_file_path):
    """
    Sets up logging configuration with the specified filename.
    Logs messages to the file defined in `log_file_path`.
    """
    logging.basicConfig(
        filename=Path(log_file_path),
        level=logging.DEBUG,  # You can adjust the logging level (DEBUG, INFO, etc.)
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def reset_logging():
    """
    Reset logging.
    """
    logging.basicConfig(level=logging.WARN)


def calculate_darkness(*, image_rgb, mask):
    """
    Function to calculate the average intensity of the masked region.
    """
    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    # Apply the mask to the grayscale image
    masked_image = cv2.bitwise_and(grayscale_image, grayscale_image,
                                   mask=mask.astype(np.uint8) * 255)
    # Calculate the average pixel intensity (darkness)
    masked_pixels = masked_image[masked_image > 0]
    # Default to white if no pixels
    average_intensity = np.mean(masked_pixels) if masked_pixels.size > 0 else 255
    return average_intensity


def process_image(*,
                  in_filepath,
                  out_filepath,
                  log_file_path="process.log",
                  largest_mask_index=1,
                  min_area_threshold=160000):
    """
    Processes an image located at the given file path and logs the processing steps.

    Parameters:
    -----------
    filepath : str or Path
        The path to the image file to be processed.

    log_file_path : str or Path, optional, default="process.log"
        The path to the log file where processing information will be recorded.
        If not specified, the default log file "process.log" will be used.

    largest_mask_index : int, optional, default=1
        The index of the largest mask to be considered during the image processing.
        This parameter is used if there are multiple masks in the image.

    min_area_threshold : int, optional, default=160000
        The minimum area threshold (in pixels) for a mask to be considered valid.
        Masks with areas smaller than this threshold will be ignored.

    Returns:
    --------
    This function does not return anything.

    Notes:
    ------
    - The function logs key events during the image processing to the specified log file.
    - The function assumes that the input image is preprocessed using smc_benchmark.preprocess
    """

    setup_logging(log_file_path)

    try:
        image_bgr = cv2.imread(in_filepath)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        # Generate masks
        sam_result = mask_generator.generate(image_rgb)

        # Sort masks by area (descending order)
        sorted_masks = sorted(sam_result, key=lambda x: x['area'], reverse=True)

        # Filter out masks that are smaller than the minimum area threshold
        filtered_masks = [mask_data for mask_data in sorted_masks if mask_data['area'] >= min_area_threshold]

        # Select the top masks and calculate their "darkness" based on average intensity
        mask_darkness = []
        for mask_data in filtered_masks:
            segmentation = mask_data['segmentation']
            darkness = calculate_darkness(image_rgb=image_rgb,
                                          mask=segmentation)
            mask_darkness.append((mask_data, darkness))

        # Sort by darkness (ascending order), so the darkest comes first
        mask_darkness.sort(key=lambda x: x[1])

        # Select the mask based on the darkness criterion
        if len(mask_darkness) >= largest_mask_index:
            selected_mask_data = mask_darkness[largest_mask_index - 1]  # Subtract 1 for 0-based indexing
            selected_mask = selected_mask_data[0]['segmentation']

            # Create a cutout of the object using the selected mask
            cutout = cv2.bitwise_and(image_rgb, image_rgb, mask=selected_mask.astype(np.uint8) * 255)

            # Create a white background
            white_background = np.ones_like(image_rgb) * 255

            # Place the cutout on the white background
            mask_inv = cv2.bitwise_not(selected_mask.astype(np.uint8) * 255)
            white_background = cv2.bitwise_and(white_background, white_background, mask=mask_inv)
            cutout_on_white = cv2.add(white_background, cutout)

            # Save the cutout of the object on the white background
            cv2.imwrite(str(out_filepath), cutout_on_white)
            logging.info(
                f"{largest_mask_index}th largest and darkest object cutout saved to {str(out_filepath)}.")
        else:
            logging.warning(
                f"Not enough valid masks in {in_filepath} to select the {largest_mask_index}th largest mask.")

    except Exception as e:
        logging.error(f"Error processing {in_filepath}: {str(e)}")
    reset_logging()


def segment_images(*,
                   input_folder,
                   output_folder,
                   log_file_path='process.log'):

    setup_logging(log_file_path)

    output_folder = str(output_folder)

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process images sequentially
    for filename in os.listdir(input_folder):
        if filename.endswith(".bmp"):
            in_filepath = Path(input_folder) / filename
            out_filepath = Path(output_folder) / filename
            process_image(in_filepath=in_filepath,
                          out_filepath=out_filepath,
                          log_file_path=log_file_path)

    reset_logging()
