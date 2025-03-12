# -*- coding: utf-8 -*-
"""
@author: Andreas Gebhard, andreas.gebhard@ivw.uni-kl.de
"""
# standard library imports
import argparse

# local application imports
from smc_benchmark.sort import sort_image_dir

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--excel", type=str, required=True,
                    help=f"Path to excel test plan")
parser.add_argument("-i", "--indir", type=str, required=True,
                    help=f"Path to input image directory")
parser.add_argument("-o", "--outdir", type=str, required=True,
                    help=f"Path to output directory")
parser.add_argument("-n", "--institution", type=str, required=True,
                    help=f"Name of the institution")
args = parser.parse_args()

sort_image_dir(excel=args.excel, indir=args.indir, outdir=args.outdir, institution=args.institution)
