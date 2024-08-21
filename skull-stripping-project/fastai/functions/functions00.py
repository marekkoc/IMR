import os
import sys
import pickle
import platform
from pathlib import Path


 

if platform.node() == 'mmiv-ml-titan':
    PATH_ROOT_DATA = Path(f'/data-10tb/shared/skull/train-3d-iso')
    PATH_GIT_HUB = Path(f'/data-10tb/marek/github_codes/skull-stripping-1/fastai')
    PATH_2D = Path(f'/data-10tb/shared/skull/')
    HOST = platform.node()

elif platform.node() == 'MMIV-DGX-Station1':
    PATH_ROOT_DATA = Path(f'/data-external/sathiesh/brains')
    PATH_GIT_HUB = Path(f'/home/marek/github/skull-stripping-1/fastai')
    PATH_2D = Path(f'/data-external/sathiesh/brains')
    HOST = platform.node()
else:
    print('Unknown host!!!!')
    sys.exit(0)
    
    
# Dictionary filling
DCT = {}
DCT[f'HOST'] = HOST
DCT[f'PATH_ROOT_DATA'] = PATH_ROOT_DATA
DCT[f'PATH_GIT_HUB'] = PATH_GIT_HUB
DCT['PATH_2D'] = PATH_2D
    
###############################    
# ### Load df's if exists ### #
###############################
ixi_test_3d = PATH_GIT_HUB / '2.2_train_valid_test_sets/ixi_test_mk_3d.csv'
if ixi_test_3d.exists():
    IXI_TEST_3D = ixi_test_3d
    DCT[f'IXI_TEST_3D'] = IXI_TEST_3D
    del ixi_test_3d

    
test_3d = PATH_GIT_HUB / '2.2_train_valid_test_sets/test_mk_3d.csv'
if test_3d.exists():
    TEST_3D = test_3d
    DCT[f'TEST_3D'] = TEST_3D
    del test_3d
    
    
train_val_3d = PATH_GIT_HUB / '2.2_train_valid_test_sets/train_val_mk_3d.csv'
if train_val_3d.exists():
    TRAIN_VAL_3D = train_val_3d
    DCT[f'TRAIN_VAL_3D'] = TRAIN_VAL_3D
    del train_val_3d
    
nfbs_test_3d = PATH_GIT_HUB / '2.2_train_valid_test_sets/nfbs_test_mk_3d.csv'
if nfbs_test_3d.exists():
    NFBS_TEST_3D = nfbs_test_3d
    DCT['NFBS_TEST_3D'] = NFBS_TEST_3D
    del nfbs_test_3d
    

    
###################################    
# ### Error file (as a picke) ### #
###################################
error_files = PATH_GIT_HUB / '2.2_train_valid_test_sets/error_files'
if error_files.exists():
    ERROR_FILES = error_files
    DCT['ERROR_FILES'] = ERROR_FILES
    del error_files






######################    
# ### Functions  ### #
######################
def mk_get_host_info():
    
    folders = list([str(v) for v in DCT.values()])
    mx = len(max(folders, key=len))   

    print((mx + 30)* '*')
    print('Settings:')
    print(f'\tHOST:  {HOST}')
    print(f'\tPATH_ROOT_DATA:  {PATH_ROOT_DATA}')
    print(f'\tPATH_GIT_HUB:  {PATH_GIT_HUB}')
    print(f'\tPATH_2D: {PATH_2D}')
    print()
    print('3D NIFTI image DF paths (_mk_3D):')
    pt = DCT.get('IXI_TEST_3D', '')
    print(f'\tIXI_TEST_3D: {pt}')
    pt = DCT.get('TEST_3D', '')
    print(f'\tTEST_3D : {pt}')
    pt = DCT.get('TRAIN_VAL_3D', '')
    print(f'\tTRAIN_VAL_3D: {pt}')
    pt = DCT.get('NFBS_TEST_3D', '')
    print(f'\tNFBS_TEST_3D: {pt}')
    
    print()
    print('Error files (pickle):')
    pt = DCT.get('ERROR_FILES', '')
    print(f'\tERROR_FILES: {pt}')
    
    print((mx + 30)* '*')
    
def mk_get_error_file_list():
    if ERROR_FILES:
        infile = open(ERROR_FILES,'rb')
        new_dict = pickle.load(infile)
        infile.close()
        return new_dict