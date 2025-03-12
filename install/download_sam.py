# -*- coding: utf-8 -*-
"""
@author: Andreas Gebhard, andreas.gebhard@ivw.uni-kl.de
"""
import urllib.request
import os
from pathlib import Path

url = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"
destination_dir = Path(__file__).parent.parent / 'resources' / 'sam'
# Create destination dir, including parents, unless it exists
destination_dir.mkdir(parents=True, exist_ok=True)

destination_path = destination_dir / 'sam_vit_h_4b8939.pth'

if not destination_path.exists():
    print(f"Downloading Segment Anything Model file from {url}.")
    print(f"This file is 2.5 GB large, so this operation may take several minutes to complete.")
    urllib.request.urlretrieve(url, destination_path)
    print(f"OK, downloaded file to {destination_path}")
else:
    print("Segment Anything Model file `sam_vit_h_4b8939.pth` already exists, skipping download.")
