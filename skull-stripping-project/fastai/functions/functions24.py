import pandas as pd
from pathlib import Path

import sys
sys.path.append('functions')

from functions00 import *
#from functions01 import *


# t1 or bias
def create_pngs_df_for_mask(pngs_t1_or_bias, pngs_mask, usg, usg_txt, t1 = True):
    """
    t1_or_bias_3d_name - signle name of t1 or biascorr 3d image
    maks_3d_name - single name of mask 3d
    t1 = True for t1 of False for bias
    
    C: 2020.08.13
    M: 2020.08.13
    """
    name = 't1_path' if t1==True else 'bias_path'

    df_part = pd.DataFrame.from_dict({'image_full_path':pngs_t1_or_bias, 'mask_full_path':pngs_mask})
    df_part['usage'] = usg
    df_part['usage_txt'] = usg_txt
    df_part['root'] = df_part['image_full_path'].str.split('test', expand=True)[0]
    df_part[name] = df_part['image_full_path'].str.split('test', expand=True)[1]
    df_part[name] = '/test' + df_part[name].astype(str)

    return df_part



def file_exist2(file):        
    df = pd.read_csv(file, plane, index_col=False)
    print(Path(file).name)
    k, l = 0, df.shape[0]
    for i,m in zip(df.image_full_path, df.mask_full_path):        
        if not Path(i).exists(): print(i);
        if not Path(m).exists(): print(m);
        print(f'{k:07}/{l}', end='\r')
        k += 1
        
        
def save_df(df, plane, full_save_name, save_folder_name='2.4_train_val_2d_path_tables'):
    """
    zmiana do modulu 2.5 wzgledem 2.4
    w 2.4 nie zadziala. Zmieniono:
        - zamieniono cross na plane
        - dodano full_save_name zamiast czesiowej nazwy
        - dodano save_folder_name
    """
    save_folder1 =  PATH_GIT_HUB / save_folder_name
    save_folder1.mkdir(parents=True, exist_ok=True)
    save_folder2 = PATH_2D / plane
    save_folder2.mkdir(parents=True, exist_ok=True)

    #save_name = f'{name}-test-val-{cross}-2d.csv'    
    pth1 = save_folder1/full_save_name
    pth2 = save_folder2/full_save_name

    df.to_csv(pth1, index=False)
    df.to_csv(pth2, index=False)
        
    print('Saved files:')
    print(f'\t{pth1}')
    print(f'\t{pth2}')
        
        
def remove_fialed_files_from_csv_file(csv_file_name, replace_csv_file=False):
    """
    
    C: 2020.08.11
    M: 2020.08.11
    """
    
    print(f'\n*** {csv_file_name} ***')
    
    if 'axial' in csv_file_name: cross = 'axial'
    if 'coronal' in csv_file_name: cross = 'coronal'
    if 'sagittal' in csv_file_name: cross = 'sagittal'
    
    pth1 = f'{PATH_GIT_HUB}/2.4_train_val_2d_path_tables/{csv_file_name}'
    pth2 = PATH_2D / f'{cross}-2d/{csv_file_name}'
    
    df = pd.read_csv(pth1, index_col=None)

    print('File name ----->>> #removed files:')

    error_list = mk_get_error_file_list()
    for er in error_list:
        sh0 = df.shape[0]
        # folder + file name
        file = (Path(er).name).split('.nii.gz')[0]
        # folder name
        fold = file.split('_T1_')[0]   

        cols = df.columns
        #print(cols)
        cols = list(cols)
        cols.remove('usage')
        cols.remove('root')
        cols.remove('usage_txt')
        cols.remove('image_full_path')
        cols.remove('mask_full_path')

        for c in cols:
            df.drop(df.loc[df[c].str.contains(fold)].index, inplace=True)
            sh2 = df.shape[0]

        er1 = er.split('brains')[-1]
        print(f'   {er1} ---> {sh0-sh2}')

    if replace_csv_file:
        
            df.to_csv(pth1, index=False) 
            df.to_csv(pth2, index=False)
            
            print('Saved files:')
            print(f'\t{pth1}')
            print(f'\t{pth2}')
    
   
