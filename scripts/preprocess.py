# -*- coding: utf-8 -*-
"""
@author: Andreas Gebhard, andreas.gebhard@ivw.uni-kl.de
"""
# standard library imports
import argparse

# local application imports
from smc_benchmark.preprocess import process_images

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--excel", type=str, required=True,
                    help=f"Path to excel test plan")
parser.add_argument("-i", "--indir", type=str, required=True,
                    help=f"Path to input image directory")
parser.add_argument("-t", "--tempdir", type=str, default='temp',
                    help=f"Path to temporary directory")
parser.add_argument("-o", "--outdir", type=str, required=True,
                    help=f"Path to output directory")
parser.add_argument("-d", "--dpi", type=int, default=150,
                    help=f"Resolution of preprocessed images in dpi.")
parser.add_argument("-b", "--batchsize", type=int, default=10,
                    help=f"Batch size, defaults to 10.")
parser.add_argument("-w", "--waittime", type=float, default=0.1,
                    help=f"Wait time, defaults to 0.1 s.")
args = parser.parse_args()

process_images(input_folder=args.indir,
               output_folder=args.outdir,
               temp_folder=args.tempdir,
               target_dpi=args.dpi,
               batch_size=args.batchsize,
               wait_time=args.waittime)
