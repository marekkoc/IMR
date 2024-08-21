import os
import pandas as pd
from pathlib import Path

##############################
# ### SOME PANDA OPTIONS ### #
##############################

#pd.set_option('display.max_rows', 500)
#pd.set_option('display.max_columns', 500)
#pd.set_option('display.width', 500)
pd.set_option('max_colwidth', 100)



#print(f'Some useful functions from {__file__} are loaded')

def mk_df_files_exists(df, columns, show=True):
    """
    Find wather file EXIST or NOT in paths from df. 
    
    Input:
        - df : df
        - columns from df to check = list
        - show: bool:True - wheater prints not existing files
        
    Output:
        - return list of not existing files
        
    C: 2020.08.07
    M: 2020.08.07
    """    
    assert isinstance(columns, list), 'Cols must be a list'
    
    # list for all columns
    notexists_all = []
    
    for col in columns:
        notexists = []
        print(f'Looing for NOT EXISTING files in "df.{col}"')        
        
        files = df[col]
        for f in files:          
            if not os.path.exists(f):
                notexists.append(f)
                
        notexists_all.extend(notexists)
        if show:
            if not notexists:
                print(f'\tAll files are OK')
            else:
                for k in notexists:
                    print(k)           
        print()
    return notexists_all
    
    
def mk_remove_error_flies_from_df(df, error_file_list, column_name='t1_pth_dgx'):
    """
    Removes names of error_files from given df. Bases on error_list from Sathiesh.
    C: 2020.08.10
    M: 2020.08.10
    """
    err_files = []

    for f in error_file_list:
        f = Path(f)
        # full file name
        f = Path(f).name
        # file name without extenstion
        f.split('.nii.gz')[0]
        
        idx = df[df[column_name].str.contains(f)].index.to_list()
        if idx:
            err_files.append(f)
        df.drop(df.loc[df[column_name].str.contains(f)].index, inplace=True)
    
    print(f' *** column_name={column_name} ***')
    if err_files:
        print(f'\tRemoved follong files from the df ({len(err_files)} files): ')
        for f in err_files:
            print(f'\t\t{f}')
    else:
        print('\tNone of the files from the error_list is contained in a df!')
        
    print(f'\tNew df shape: {df.shape}\n')
    
    
def get_png_list_for_mask(path_to_3d_image, plane, train_val_test):
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


def mk_wrap_text(text, pat='*'):
    """Wrape test with a pattern.
    
    C: 2020.08.21
    M: 2020.08.21
    """
    ln = len(text)
    k = (8+ln) * pat
    print(f'{k}*{pat}\n*** {text}   ***\n{k}*{pat}')