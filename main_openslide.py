#%% Imports

import os
import time
from skimage import io 
from pathlib import Path

OPENSLIDE_PATH = r'c:\Users\bdeha\Projects\ETH-ScopeM_Ozimski\openslide-win64-20230414\bin'
if hasattr(os, 'add_dll_directory'):
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
else:
    import openslide

from openslide import OpenSlide

#%% Initialize

data_path = Path('D:\local_Ozimski\data\jpeg')
slide_name = 'slide-2023-06-08T11-13-27-R1-S14.mrxs'
slide_path = Path(data_path) / slide_name
slide = OpenSlide(slide_path)