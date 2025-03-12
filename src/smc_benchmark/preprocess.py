# -*- coding: utf-8 -*-
"""
@author: Miro Duhovic, miro.duhovic@ivw.uni-kl.de
@author: Andreas Gebhard, andreas.gebhard@ivw.uni-kl.de
"""

# standard library imports
import gc
import glob
import os
import shutil
import time

# local application imports
# none

# third party library imports
import cv2
from PIL import Image


def create_folder(folder_path):
    """
    Create a folder if it doesn't exist
    """
    os.makedirs(str(folder_path), exist_ok=True)
    print(f"Created folder: {folder_path}")


# Function to convert DPI and reduce image resolution in batches
def convert_dpi_and_resize(*,
                           input_folder,
                           output_folder,
                           target_dpi=150,
                           batch_size=10,
                           wait_time=0.1):
    # Get all image files
    image_files = glob.glob(os.path.join(input_folder, "*.bmp")) + \
                  glob.glob(os.path.join(input_folder, "*.jpg")) + \
                  glob.glob(os.path.join(input_folder, "*.jpeg")) + \
                  glob.glob(os.path.join(input_folder, "*.png"))

    # Create the output folder
    create_folder(output_folder)

    # Process images in batches
    for batch_start in range(0, len(image_files), batch_size):
        batch = image_files[batch_start:batch_start+batch_size]

        print(f"Processing batch {batch_start // batch_size + 1} with {len(batch)} images...")

        for image_path in batch:
            try:
                # Open the image
                img = Image.open(image_path)

                # Get current DPI (if available, default to 600 DPI)
                current_dpi = img.info.get('dpi', None)
                if current_dpi is None or current_dpi[0] == 0:
                    print(f"Invalid or no DPI metadata found for {image_path}. Defaulting to 600 DPI.")
                    current_dpi = (600, 600)  # Default to 600 DPI if no DPI info is found, or it's zero
                else:
                    print(f"Current DPI for {image_path}: {current_dpi}")

                # Calculate the scaling factor based on the DPI change (halving DPI from 600 to 300)
                scale_factor = target_dpi / current_dpi[0]  # Use current_dpi[0] (horizontal DPI)

                # Get the current image dimensions
                width, height = img.size

                # Calculate the new dimensions
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)

                # Resize the image to the new dimensions using LANCZOS (formerly ANTIALIAS)
                img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # Construct the output file path
                filename = os.path.basename(image_path)
                output_image_path = os.path.join(output_folder, filename)

                # Save the image with the new DPI and resized dimensions
                img_resized.save(output_image_path, dpi=(target_dpi, target_dpi))

                print(f"Converted {image_path} -> {output_image_path} with {target_dpi} DPI.")

                # Explicitly delete the image objects and run garbage collection
                del img
                del img_resized
                gc.collect()

                # Optionally, wait for a short time after each image is processed
                time.sleep(wait_time)  # Add a delay (in seconds)

            except Exception as e:
                print(f"Error processing {image_path}: {e}")

        # After processing the batch, we can optionally clear memory again
        gc.collect()

        # Optionally, wait for a short time after each batch is processed
        print(f"Waiting for {wait_time} seconds before processing the next batch...")
        time.sleep(wait_time)  # Add a delay (in seconds)


# Function to convert the image to 8-bit grayscale
def convert_to_8bit(input_folder, output_folder):
    # Process each image in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith((".jpg", ".bmp", ".jpeg", ".png")):
            try:
                # Load the image
                image_path = os.path.join(input_folder, filename)
                image = cv2.imread(image_path)

                # Convert the image to 8-bit grayscale
                grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                # Define the output path for the 8-bit grayscale image in the output folder
                grayscale_image_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '_8bit.bmp')

                # Save the 8-bit grayscale image
                cv2.imwrite(grayscale_image_path, grayscale_image)
                print(f"Converted {filename} to 8-bit grayscale as {os.path.basename(grayscale_image_path)}")
            except Exception as e:
                print(f"Error converting {filename} to 8-bit grayscale: {e}")


# Function to delete the temporary folder and its contents
def delete_temp_folder(*, folder_path):
    try:
        shutil.rmtree(folder_path)
        print(f"Deleted temporary folder: {folder_path}")
    except Exception as e:
        print(f"Error deleting temporary folder {folder_path}: {e}")


# Main function to handle the entire process
def process_images(*,
                   input_folder,
                   output_folder,
                   temp_folder,
                   target_dpi=150,
                   batch_size=10,
                   wait_time=0.1):

    # Create the output and temp folders
    create_folder(output_folder)
    create_folder(temp_folder)

    # Step 1: Resize and adjust DPI
    convert_dpi_and_resize(input_folder=input_folder,
                           output_folder=temp_folder,
                           target_dpi=target_dpi,
                           batch_size=batch_size,
                           wait_time=wait_time)

    # Step 2: Convert to 8-bit grayscale and save directly to the output folder
    convert_to_8bit(temp_folder, output_folder)

    # Step 3: Delete the temporary folder
    delete_temp_folder(folder_path=temp_folder)
