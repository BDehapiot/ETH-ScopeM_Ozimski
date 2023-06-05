#%% Imports

import os
import time
import numpy as np
from skimage import io 
from pathlib import Path
from joblib import Parallel, delayed 

#%% Parameters

rSize_factor = 6

tWinSize = 51 
tWinSize = tWinSize // rSize_factor
tWinSize = tWinSize if tWinSize % 2 != 0 else tWinSize + 1
minObjects = 65636 // rSize_factor
minHoles = 1024 // rSize_factor

#%% Initialize

from skimage.transform import downscale_local_mean

# -----------------------------------------------------------------------------

slide_name = 'slide-2023-05-22T11-12-01-R1-S22'
C1_name = slide_name + '_Wholeslide_Alexa 488_Extended.tif'
C2_name = slide_name + '_Wholeslide_Alexa 633_Extended.tif'
C3_name = slide_name + '_Wholeslide_DAPI_Extended.tif'
C1_path = Path('data', 'j2k', slide_name + '_TIFF') / C1_name
C2_path = Path('data', 'j2k', slide_name + '_TIFF') / C2_name
C3_path = Path('data', 'j2k', slide_name + '_TIFF') / C3_name
paths = [C1_path, C2_path, C3_path]

# -----------------------------------------------------------------------------

start = time.time()
print('Load image')

C1_img = io.imread(C1_path)
C2_img = io.imread(C2_path)
C3_img = io.imread(C3_path)

C1_rSize = downscale_local_mean(
    C1_img, (rSize_factor, rSize_factor)).astype('uint8')
C2_rSize = downscale_local_mean(
    C2_img, (rSize_factor, rSize_factor)).astype('uint8')
C3_rSize = downscale_local_mean(
    C3_img, (rSize_factor, rSize_factor)).astype('uint8')

end = time.time()
print(f'  {(end-start):5.3f} s')

#%%

from skimage.measure import label, regionprops
from skimage.morphology import (
    binary_erosion, binary_dilation, remove_small_objects, remove_small_holes
    )
from skimage.filters import (
    threshold_triangle, threshold_niblack, threshold_sauvola, gaussian
    )

start = time.time()
print('Process image')

gblur = gaussian(C1_rSize + C2_rSize + C3_rSize ,2)
mask = threshold_niblack(gblur, window_size=tWinSize, k=0.2) > 0.1
mask = remove_small_objects(mask, min_size=minObjects)
mask = remove_small_holes(mask, area_threshold=minHoles)
mask = binary_dilation(mask ^ binary_erosion(mask))

import napari
viewer = napari.Viewer()
viewer.add_image(C1_rSize, contrast_limits=(0, 40))
viewer.add_image(C2_rSize, contrast_limits=(0, 40))
viewer.add_image(C3_rSize, contrast_limits=(0, 255))
viewer.add_image(mask, blending='additive', colormap='red')

end = time.time()
print(f'  {(end-start):5.3f} s')

#%%

labeled = label(mask)
props = regionprops(labeled)
labels = [prop['label'] for prop in props]
areas = [prop['area'] for prop in props]


#%%

# import napari
# viewer = napari.Viewer()
# viewer.add_image(C1_rSize)
# viewer.add_image(C1_mask)
# viewer.add_image(C2_rSize)
# viewer.add_image(C3_rSize)