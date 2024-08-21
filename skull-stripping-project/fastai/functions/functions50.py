import os
import time
import glob
import pandas as pd
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

from pathlib import Path
from skimage.color import gray2rgb
from sklearn.metrics import jaccard_score



###########################
# ### DB manipulation ### #
###########################
def get_db_names(df, col='db'):
    """Get all DB names present in a df

    Parametrs:
    df (pandas df): An entire df, with all 2D slices
    
    Returns:
    list: DB names
    
    MMIV-ML
    C: 2020.08.16
    M: 2020.08.17
    """
    return list(df[col].unique())


def get_single_db(df, db_name):
    """Get df and indices of selected DB (all 2d slices that belong to this DB).
    
    Parameters:
    df (pandas df): An entire df, with all 2D slices
    db_name (string): Name of specified db e.g. 'ADNI'
        
    Returns:
    df : All entracnes from specified DB
    pandas.core.indexes.numeric.Int64Index : Indices within of 2d slices of all patients (examinations) that belong to specified db
    
    
    C: 2020.08.16
    M: 2020.08.17
    """
    idx_db = df[df['db'].str.contains(db_name)].index
    dfn = df[df['db'].str.contains(db_name)]
    return dfn, idx_db


def get_all_patient_list_from_df(df):
    """Get pattern list that belong to a full df (or a single db, e.g. ADNI)
    
    Parameters:
    df (pandas df): An entire df or df only with one db e.g. ADNI (with all 2D slices).
            
    Returns:
    pattern (list) : List of patients within df (or a single DB)
    
    
    C: 2020.08.16
    M: 2020.08.17
    """    
    # A list of all patients in all db's
    pattern = list(df.patient.unique())
    return pattern


def get_one_patient(df, path_to_slices):
    """Get df and indices of 2d slices that belong to a specified patient - based on 'pattern'.
    
    Parameters:
    df (pandas df): An entire df or df only with one db e.g. ADNI (with all 2D slices).
    path_to_slices (string): Column 'part' fro df. String pattern to name common part for all 2d slices
                            within one pateint (full path without slce number _001.png)
        
    Returns:
    pandas.core.indexes.numeric.Int64Index : Indices within of 2d slices of one patient
    
    
    C: 2020.08.16
    M: 2020.08.7
    """
    path_to_slices = str(path_to_slices)

    # find indices
    #idx = df[df['full'].str.contains(path_to_slices)].index
    # get the singe axam
    df_exam = df[df['full'].str.contains(path_to_slices)]
    idx = df_exam.index
    return df_exam, idx


############################
# ### png's for a mask ### #
############################
def get_pngs_for_mask(path_to_3d_image, plane, train_val_test):
    """
    for a sigle 3d_nii.gz mask image, gets all existing 2d slices with png extention
    
    C: 2020.08.12
    M: 2020.08.21
    """
    
    r1,r2 = path_to_3d_image.split('train-3d-iso')
    r1 = Path(r1)
    tmp = r2.split('/')
    data = tmp[1]
    subject = tmp[2].split('_T1_')[0]
    filename_nii = tmp[2].split('.anat_')[1]
    filename = filename_nii.split('.nii')[0]

    path2d = r1/plane/train_val_test/data/subject/filename    
    png_list = sorted(glob.glob(f'{path2d}*.png'))
    return png_list

###################################
# ### save an image  as Nifti ### #
###################################
def mkSaveImageAsNifti(data,niftioriginal,name):
    hdr = niftioriginal.header
    hdr['descrip'] = 'MMIV/ML-nib: ' + nib.__version__ + '-by MK ({})'.format(time.strftime("%Y-%m-%d"))
    img = nib.Nifti1Image(data, affine=niftioriginal.affine, header=hdr)
    img.set_data_dtype(data.dtype.name)
    img.to_filename(name)
    #print("\tImage saved as %s"%name)
    
    

def save_128_as_nifti(patient_pattern, image, suffix_name, test_name, save_root_folder):
    """
    Saves 3D image (selected examination 128x128xN) as a nifti file.
    
    Updates voxel dimension (to check!)
    
    Parameters:
    - patient_pattern [str] : common name for all 2d slices without sclice number (without *_000.png)
                             e.g. /data-10tb/shared/skull/axial-2d//test/PPMI/PPMI_3114_MR_T1-anatomical_Br_20120905120705829_S120901_I330555.anat/T1_biascorr_iso_
    - image [np.array] : 3d images to save. Image (x), predictions (p) or FSL output (y).    
    - test_name [str] : path to applied test set,
                        e.g. TEST_3D, IXI_TEST_3D to load approprioate CSV file to get path to oryginal FSL mask (nii image)    
    - saver_root_folder [str:Path] : path to root save folder (e.g. SAVE_PTH_301_DATA)    
    - suffix_name [str] : to distinguish among: image (x), FSL mask (y) and prediction (p).
    
    Returns:
    None    
    
    C: 2020.08.15
    M: 2020.08.20
    """
    # exam name:  PPMI_3114_MR_T1-anatomical_Br_20120905120705829_S120901_I330555.anat
    exam_name, file_name = patient_pattern.split('/')[-2:]
    #print(exam_name)
    #print(file_name)
    
    # table with 3D path images for DGX and Titan (based on Sathies'h table)
    df_masks = pd.read_csv(test_name)
    #df_masks.head()
    
    # czesc df (wszystkie kolumny) ktore zawieraja szukanego pacjenta
    cur_msk_3d = df_masks[df_masks['mask_nn_pth_titan'].str.contains(exam_name)]
    # lista wszyskiech masek (lista z jednym elementem)
    cur_mask = cur_msk_3d.mask_nn_pth_titan
    # odczytanie sciezki do maski
    nii = nib.load(cur_mask.values[0])
    # oryginalny naglowek i rozmiary obrazu
    hdr =  nii.header    
    d1, d2, d3 = hdr['dim'][1:4]
    #print(d1, d2)    
    #print(hdr['pixdim'])

    hdr['descrip'] = 'MMIV-ML-nib: ' + nib.__version__ + '-by MK ({})'.format(time.strftime("%Y-%m-%d"))
    img = nib.Nifti1Image(image, affine=np.eye(4), header=hdr)
    img.set_data_dtype(image.dtype.name)
    # nowy naglowek
    hdr = img.header
    # nowe rozmiary pixela, to trzeba sprawdzic, bo zrobione jest na czuja!!!
    hdr['pixdim'][1:4] = (128/d2, 128/d1, 128/d3)
    
    for db in ['ADNI', 'AIBL', 'IXI', 'PPMI', 'SALD', 'SLIM', 'CalgaryCampinas']:
        if db in patient_pattern:
            save_folder = db
            break
            
    # /data-10tb/shared/skull/pred/3.01/test_3D/PPMI/
    save_path = Path(save_root_folder) / save_folder
    save_path.mkdir(parents=True, exist_ok=True)
    
    #PPMI_3114_MR_T1-anatomical_Br_20120905120705829_S120901_I330555.anat_T1_biascorr_iso_x.nii.gz
    save_file = f'{exam_name}_{file_name}{suffix_name}.nii.gz'
    pth = save_path / save_file
    
    # save to a file
    img.to_filename(pth)
    print(f'*** Saved: {pth}')

    
    
################
# ### Dice ### #
################
def dice(im1, im2):
    """
    Computes the Dice coefficient, a measure of set similarity.
    Parameters
    ----------
    im1 : array-like, bool
        Any array of arbitrary size. If not boolean, will be converted.
    im2 : array-like, bool
        Any other array of identical size. If not boolean, will be converted.
    Returns
    -------
    dice : float
        Dice coefficient as a float on range [0,1].
        Maximum similarity = 1
        No similarity = 0
        
    Notes
    -----
    The order of inputs for `dice` is irrelevant. The result will be
    identical if `im1` and `im2` are switched.
    
    https://gist.github.com/JDWarner/6730747
    """
    im1 = np.asarray(im1).astype(np.bool)
    im2 = np.asarray(im2).astype(np.bool)

    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1 and im2 must have the same shape.")

    # Compute Dice coefficient
    intersection = np.logical_and(im1, im2)

    return 2. * intersection.sum() / (im1.sum() + im2.sum())


def print_dice_jaccard_1(df3d):
    """Prints Dice and Jaccard coefficients.
    
    C: 2020.08.17
    M: 2020.08.22
    """
    dice = np.array(df3d.dice)
    jaccard = np.array(df3d.jaccard)
    hausdorff = np.array(df3d.hausdorff)

    k=70
    print(k*'*')
    print('Global:')
    print(f'    Dice:       max={dice.max():.4f}, min={dice.min():.4f}, | mean={dice.mean():.4f}, std={dice.std():.4f}')
    print(f'    Jaccard:    max={jaccard.max():.4f}, min={jaccard.min():.4f}, | mean={jaccard.mean():.4f}, std={jaccard.std():.4f}')
    print(f'    Hausdorff    max={hausdorff.max():.4f}, min={hausdorff.min():.4f}, | mean={hausdorff.mean():.4f}, std={hausdorff.std():.4f}')
    print(k*'*')

    dbs = get_db_names(df3d)
    for db in dbs:
        df_db, idxn = get_single_db(df3d, db)    
        dice_db= df3d.loc[idxn, 'dice']
        jaccard_db= df3d.loc[idxn, 'jaccard']
        hausdorff_db= df3d.loc[idxn, 'hausdorff']

        print(f'{db}:')
        print(f'    Dice:       max={dice_db.max():.4f}, min={dice_db.min():.4f}, | mean={dice_db.mean():.4f}, std={dice_db.std():.4f}')
        print(f'    Jaccard:    max={jaccard_db.max():.4f}, min={jaccard_db.min():.4f}, | mean={jaccard_db.mean():.4f}, std={jaccard_db.std():.4f} ')
        print(f'    Hausdorff:  max={hausdorff_db.max():.4f}, min={hausdorff_db.min():.4f}, | mean={hausdorff_db.mean():.4f}, std={hausdorff_db.std():.4f}')
    print(k*'*')


def _print_coefs(df3d, name, coef, param):
    """
    C: 2020.08.22
    M: 2002.08.22
    """
    k=45
    print()
    print(f'{name:*^45}')
    print(f'      |  max,     min   |     mean,     std ')
    print(f'GLOB. | {param.max():.4f},    {param.min():.4f}, |    {param.mean():.4f},    {param.std():.4f}')
    print(k*'*')
    dbs = get_db_names(df3d)
    for db in dbs:
        df_db, idxn = get_single_db(df3d, db)    
        param_db= df3d.loc[idxn, coef ]        

        print(f'{db}:', end=' | ')
        print(f'{param_db.max():.4f},    {param_db.min():.4f}, |    {param_db.mean():.4f},    {param_db.std():.4f}')
    print(k*'*')
    
    
def print_dice_jaccard_2(df3d, print_dice=True, print_jaccard=False, print_hausdorff=False):
    """Prints Dice and Jaccard coefficients.
    
    C: 2020.08.17
    M: 2020.08.22
    """
    dice = np.array(df3d.dice)
    jaccard = np.array(df3d.jaccard)
    hausdorff = np.array(df3d.hausdorff)

    df3d['db'].replace('CalgaryCampinas', 'CC  ', inplace=True)
    
    if print_dice:        
#         name = ' Dice ', coef = 'dice', param  = dice
        _print_coefs(df3d, ' Dice ', 'dice', dice)
    
    if print_jaccard:        
        _print_coefs(df3d, ' Jaccard ', 'jaccard', jaccard)
    
    if print_hausdorff:                
        _print_coefs(df3d, ' Hausdorff ', 'hausdorff', hausdorff)
        

def get_biggest_smallest_dice_jaccard_coefs(df_3d, db='ALL', sort_column='dice', max_min = 'max', N=5):
    
    """Find N the smallest/biggest values of dice or jaccard in a given df_3d
    
    Parameters:
    - df_3d [pandas df] : dataframe with dice and jaccard coeficients    
    - db [str] : database name (e.g. 'ADNI', 'PPMI') to search in or 'ALL' for the entire df_3d    
    - sort_column [str] : name of column to sort by; 'dice' or 'jaccard'    
    - N [int] : number of the first N element to select from a sorted df    
    - min_max ['str'] : 'max' or 'min', to search fro the biggest or the smallest elements in a df    
    
    Returns:
    - df - sorted df (selected N rows of the entire df_3d)
    - idx - indexes in the df_3d of selectesd rows    
    
    C: 2020.08.20
    M: 2020.08.20    
    """
    ### Find N the smallest/biggest values of dice or jaccard
    df_3d.head(10)
    #print(df_3d.shape)

    # choose a signle db or entire df
    if db == 'ALL':
        df_sort = df_3d
        print(f'*** Search for the entire df ***')
    else:
        df_sort= df_3d[df_3d['db']==db]
        print(f'*** Search for {db} ***')

    # sort by dice or jaccard
    if max_min == 'min':
        df_sort = df_sort.sort_values(by=sort_column, ascending=True)
    else:
        df_sort= df_sort.sort_values(by=sort_column, ascending=False)

    print(f'\tSort column: {sort_column.upper()}')

    # select N the biggest/smallest items and its indices
    df_sort = df_sort.iloc[:N,:]
    idxs = df_sort.iloc[:N, :].index
    print(f'\tSelect: {N} {max_min.upper()} items')
    print()
    return df_sort, idxs

#########################
# ### Visualization ### #
#########################
def vis_2d_from_slice_rgb(y, x, p, cmap='Reds', tit=['FSL', 'Prediction', 'FSL(red), prediction(green)'], **kw):
    """
    Shows owerlapped FSL and prediction masks on the orignal image as RGB channesl (mask is red). Works on 2D slices.
    
    C: 2020.08.16
    M: 2020.08.19
    """
    
    figsize = kw.get('figsize', (10,8))
    
    rgb1 = gray2rgb(x, False)
    xx1,yy1 = np.where(y==1)
    rgb1[xx1,yy1,0] = 1
    
    rgb2 = gray2rgb(x, True)
    xx2,yy2 = np.where(p==1)
    rgb2[xx2,yy2,1] = 1
    
    rgb3 = np.zeros_like(rgb1)
    rgb3[:,:,0] = y
    rgb3[:,:,1] = p
    
    rgb = [rgb1, rgb2, rgb3]
    
    plt.figure(figsize=figsize)
    for i in range(3):
        plt.subplot(1,3,i+1)
        plt.imshow(rgb[i])
        plt.title(tit[i])
        plt.axis('off')
    plt.tight_layout()
    
    
def vis_2d_from_slice(y, x, p, cmap='gray', tit=['FSL', 'Image', 'Prediction'], **kw):
    """
    Shows FSL, image and prediction images separately. Works on 2D slices.
    
    C: 2020.08.16
    M: 2020.08.19
    """
    figsize = kw.get('figsize', (10,8))
    
    im = [y, x, p]
    plt.figure(figsize=figsize)
    for i in range(3):
        plt.subplot(1,3,i+1)
        plt.imshow(im[i], cmap=cmap)
        plt.title(tit[i])
        plt.axis('off')
    plt.tight_layout()
    

def vis_3d(y, x, p, k, cmap='gray', tit=['FSL', 'Image', 'Prediction'], **kw):
    """
    Visiualization from 3D image (single examination)
    
    C: 2020.08.16
    M: 2020.08.21
    """
    aspect = kw.get('aspect', 1)
    figsize = kw.get('figsize', (8,3))
    save_pth = kw.get('save_pth', None)
    suptitle = kw.get('suptitle', None)
    
    if suptitle:
        suptitle = f'{suptitle}; slice:{k}'
    
    if save_pth:
        if save_pth.suffix:
            save_pth = str(save_pth) + '_bw.png'
            #save_pth=f'{save_pth}_rgb.png'
        else:
            save_pth=f'{save_pth}_bw.png'
    
    
    im = [y, x, p]    
    plt.figure(figsize=figsize)
    for i in range(3):
        plt.subplot(1,3,i+1)
        img = np.rot90(im[i][k,:,:])**.5
        plt.imshow(img, cmap=cmap)
        plt.title(tit[i])
        plt.axis('off')
    #plt.tight_layout()
    if suptitle:
        plt.suptitle(suptitle)
    if save_pth:
        plt.savefig(save_pth, bbox_inches='tight', pad_inches=0.2)
    
def vis_3d_rgb(yP, xP, pP, k, tit=['FSL', 'Prediction', 'FSL(red), prediction(green)'], **kw):
    """
    Shows owerlapped FSL and prediction masks on the orignal image as RGB channesl (mask is red). Works on 3D images.
    
    C: 2020.08.16
    M: 2020.08.21
    """
    aspect = kw.get('aspect', 1)
    figsize = kw.get('figsize', (8,3))
    save_pth = kw.get('save_pth', None)
    suptitle = kw.get('suptitle', None)
    
    if suptitle:
        suptitle = f'{suptitle}; slice:{k}'
    
    if save_pth:
        if save_pth.suffix:
            save_pth = str(save_pth)
            #save_pth=f'{save_pth}_rgb.png'
        else:
            save_pth=f'{save_pth}_rgb.png'
    
    x = xP[k,:,:] ** .5
    y = yP[k,:,:]
    p = pP[k,:,:]
    
    rgb1 = gray2rgb(x, False)
    xx1,yy1 = np.where(y==1)
    rgb1[xx1,yy1,0] = 1
    
    rgb2 = gray2rgb(x, True)
    xx2,yy2 = np.where(p==1)
    rgb2[xx2,yy2,1] = 1
    
    rgb3 = np.zeros_like(rgb1)
    rgb3[:,:,0] = y
    rgb3[:,:,1] = p
    
    rgb = [rgb1, rgb2, rgb3]    
    f, ax = plt.subplots(1,3,figsize=figsize)
    if suptitle:
        plt.suptitle(suptitle)
    for i in range(3):
        ax[i].imshow(np.rot90(rgb[i]))
        ax[i].set_title(tit[i])
        ax[i].axis('off')
        ax[i].set_aspect(aspect, 'box')
    #plt.tight_layout()
    
    if save_pth:
        plt.savefig(save_pth, bbox_inches='tight', pad_inches=0.2);
        print(f'Saved file: {save_pth}')