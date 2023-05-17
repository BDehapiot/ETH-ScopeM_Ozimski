#%% Imports

import os
import time
from skimage import io 
from pathlib import Path

OPENSLIDE_PATH = r'c:\Users\bdeha\Projects\ETH-ScopeM_Ozimski\openslide-win64-20230414\bin'
if hasattr(os, 'add_dll_directory'):
    # Python >= 3.8 on Windows
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
else:
    import openslide
    
from openslide import OpenSlide

#%% Initialize

slide_name = 'slide-2023-05-15T11-23-48-R1-S15.mrxs'
slide_path = Path('data', 'raw') / slide_name
slide = OpenSlide(slide_path)


