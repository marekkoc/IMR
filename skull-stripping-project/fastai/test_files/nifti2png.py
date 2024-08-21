#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 20:41:10 2020
@author: marek

C: 2020.05.19
M: 2020.05.20

C: MMIV-ML
"""

import os
import glob
from pathlib import Path
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import imageio as io


#p = Path('/data-10tb/marek/IXI/').glob('*/*/T1*rr.nii.gz')


img_name = 'T1_biascorr.nii.gz'
msk_name = 'T1_biascorr_brain_mask.nii.gz'

root_folder = Path('/data-10tb/marek/IXI/train_data/FSL_outputs/')
images_list = root_folder.glob(f'*/{img_name}')
masks_list = root_folder.glob(f'*/{msk_name}')

save_root_folder = Path('/data-10tb/marek/IXI/fastai/data2d')
save_root_folder.mkdir(parents=True, exist_ok=True)


for img_full_path, msk_full_path in zip(images_list, masks_list):

    # Get the name, e.g.: IXI422-Guys-1071-T1.anat
    exam_name = img_full_path.parent.name

    images_folder = save_root_folder / 'images'
    images_folder.mkdir(exist_ok=True)

    masks_folder = save_root_folder / 'labels'
    masks_folder.mkdir(exist_ok=True)

    image = nib.load(img_full_path).get_fdata()
    mask = nib.load(msk_full_path).get_fdata() 
    mask = mask.astype('uint8')

    # get a 'raw' image name (without .nii.gz)
    fn1 = img_full_path.stem
    fn2 = fn1.split('.')[0]

    # all slices in each image
    if 1:
        # save slices to savefolder
        for k in range(image.shape[0]):
            png_name_img = f'{exam_name}_{fn2}_{k:03}.png'
            png_name_msk = f'{exam_name}_{fn2}_{k:03}_M.png'

            save_folder_img = images_folder / png_name_img
            plt.imsave(save_folder_img, image[k, :, :], cmap='gray')

            save_folder_msk = masks_folder / png_name_msk
            io.imsave(save_folder_msk, mask[k, :, :])

            print(png_name_img)
            print(png_name_msk)
    # selected slice
    if 0:
        x,y,z = image.shape
        k = x//2

        png_name_img = f'{exam_name}_{fn2}_{k:03}.png'
        png_name_msk = f'{exam_name}_{fn2}_{k:03}_M.png'

        print(png_name_img)
        print(png_name_msk)

        save_folder_img = images_folder / png_name_img
        plt.imsave(save_folder_img, image[k, :, :], cmap='gray')

        save_folder_msk = masks_folder / png_name_msk
        io.imsave(save_folder_msk, mask[k, :, :]) 

