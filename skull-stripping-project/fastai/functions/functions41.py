import numpy as np
import imageio as io
import nibabel as nib
import matplotlib.pyplot as plt
from pathlib import Path



def axial_3d_2_2d(path_to_3d_image, index):
        
    r1,r2 = path_to_3d_image.split('train-3d-iso')
    r1 = Path(r1)
    tmp = r2.split('/')
    data = tmp[1]
    subject = tmp[2].split('_T1_')[0]
    filename_nii = tmp[2].split('.anat_')[1]
    filename = filename_nii.split('.nii')[0]
    
    path2d = r1/'axial-2d'/'test'/data/subject
    path2d.mkdir(parents=True, exist_ok=True)
    
    im3d = nib.load(path_to_3d_image).get_fdata()
    
    ### STANDARYZACJA
    im3d -= im3d.mean()
    im3d /= im3d.std()
    
    sl = im3d.shape[2]
    
    # T1 or MASK image
    if 'mask' in filename:
        mask = True
        im3d = im3d.astype(np.uint8)
    else:
        mask = False
    
    for k in range(sl):
        filename_png = f'{filename}_{k:03}.png'
        path_png = path2d/filename_png
        
        if mask:
            io.imsave(path_png, np.where(im3d[:,:,k]>=1, 1, 0).astype(np.uint8))      
        else:
            plt.imsave(path_png, im3d[:,:,k], cmap='gray')
            
        
def coronal_3d_2_2d(path_to_3d_image, index):
    
    
    r1,r2 = path_to_3d_image.split('train-3d-iso')
    r1 = Path(r1)
    tmp = r2.split('/')
    data = tmp[1]
    subject = tmp[2].split('_T1_')[0]
    filename_nii = tmp[2].split('.anat_')[1]
    filename = filename_nii.split('.nii')[0]
    
    path2d = r1/'coronal-2d'/'test'/data/subject
    path2d.mkdir(parents=True, exist_ok=True)
    
    im3d = nib.load(path_to_3d_image).get_fdata()
    
    ### STANDARYZACJA   
    im3d -= im3d.mean()
    im3d /= im3d.std()
    
    sl = im3d.shape[1]
    
    # T1 or MASK image
    if 'mask' in filename:
        mask = True
        im3d = im3d.astype(np.uint8)
    else:
        mask = False
    
    for k in range(sl):
        filename_png = f'{filename}_{k:03}.png'
        path_png = path2d/filename_png
        
        if mask:
            io.imsave(path_png, np.where(im3d[:,k,:]>=1, 1, 0).astype(np.uint8))      
        else:
            plt.imsave(path_png, im3d[:,k,:], cmap='gray')
            
            
def sagittal_3d_2_2d(path_to_3d_image, index):
    
    
    r1,r2 = path_to_3d_image.split('train-3d-iso')
    r1 = Path(r1)
    tmp = r2.split('/')
    data = tmp[1]
    subject = tmp[2].split('_T1_')[0]
    filename_nii = tmp[2].split('.anat_')[1]
    filename = filename_nii.split('.nii')[0]
    
    path2d = r1/'sagittal-2d'/'test'/data/subject
    path2d.mkdir(parents=True, exist_ok=True)
    
    im3d = nib.load(path_to_3d_image).get_fdata()
    
    ### STANDARYZACJA   
    im3d -= im3d.mean()
    im3d /= im3d.std()
    
    sl = im3d.shape[0]
    
    # T1 or MASK image
    if 'mask' in filename:
        mask = True
        im3d = im3d.astype(np.uint8)
    else:
        mask = False
    
    for k in range(sl):
        filename_png = f'{filename}_{k:03}.png'
        path_png = path2d/filename_png
        
        if mask:
            io.imsave(path_png, np.where(im3d[k,:,:]>=1, 1, 0).astype(np.uint8))       
        else:
            plt.imsave(path_png, im3d[k,:,:], cmap='gray')
            
            