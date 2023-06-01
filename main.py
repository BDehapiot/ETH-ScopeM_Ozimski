#%% Imports

import os
import time
import numpy as np
from skimage import io 
from pathlib import Path
from joblib import Parallel, delayed 

#%% Parameters

rSize_factor = 20
thresh_coeff = 2

#%% Initialize

from skimage.filters import threshold_otsu, gaussian
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

C1_thresh = threshold_otsu(gaussian(C1_rSize, 5))
C1_mask = C1_rSize > C1_thresh * thresh_coeff

end = time.time()
print(f'  {(end-start):5.3f} s')

#%%

import napari
viewer = napari.Viewer()
viewer.add_image(C1_rSize)
viewer.add_image(C1_mask)
# viewer.add_image(C2_rSize)
# viewer.add_image(C3_rSize)