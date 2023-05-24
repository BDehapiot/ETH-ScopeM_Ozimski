#%% Imports

import os
import time
import numpy as np
from skimage import io 
from pathlib import Path

OPENSLIDE_PATH = r'c:\Users\bdeha\Projects\ETH-ScopeM_Ozimski\openslide-win64-20230414\bin'
if hasattr(os, 'add_dll_directory'):
    with os.add_dll_directory(OPENSLIDE_PATH):
        import openslide
else:
    import openslide
from openslide import OpenSlide, open_slide

#%% Initialize

from skimage.transform import rescale, downscale_local_mean


slide_name = 'slide-2023-05-22T11-12-01-R1-S22_Wholeslide_Alexa 488_Extended.tif'
slide_path = Path(
    'data', 'jpeg', 'slide-2023-05-22T11-12-01-R1-S22_TIFF'
    ) / slide_name

# -----------------------------------------------------------------------------

start = time.time()
print('Load image')

img = io.imread(slide_path)

end = time.time()
print(f'  {(end-start):5.3f} s')

# -----------------------------------------------------------------------------

start = time.time()
print('Downscale image')

img = downscale_local_mean(img, (10, 10)).astype('uint8')

end = time.time()
print(f'  {(end-start):5.3f} s')

#%% Initialize

# slide_name = 'slide-2023-05-22T09-49-41-R1-S22.mrxs'
# slide_path = Path('data', 'bmp') / slide_name
# slide = OpenSlide(slide_path)

# slide_props = slide.properties
# pixSize = slide_props['openslide.mpp-x']
# imgSize = slide.dimensions

#%%

import napari
viewer = napari.Viewer()
viewer.add_image(img)