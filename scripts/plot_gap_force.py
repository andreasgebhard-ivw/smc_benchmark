# -*- coding: utf-8 -*-
"""
@author: Andreas Gebhard, andreas.gebhard@ivw.uni-kl.de
"""
# standard library imports
import argparse

# local application imports
from smc_benchmark.plot import plot_gap_force

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dpi", type=int, default=300,
                    help=f"Resolution of the plots in dpi")
parser.add_argument("-i", "--indir", type=str, required=True,
                    help=f"Path to data directory")
parser.add_argument("-o", "--outdir", type=str, default=None,
                    help=f"Path to output directory")
parser.add_argument("-n", "--institution", type=str, required=True,
                    help=f"Name of the institution")
args = parser.parse_args()

plot_gap_force(indir=args.indir, outdir=args.outdir,
               institution=args.institution, dpi=args.dpi)
