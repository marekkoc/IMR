# MMIV_ML
#
#
# C: 2020.09.07
# M: 2020.09.11
#

import pandas as pd
import nibabel as nib
import numpy as np

def get_ixi_info(ixi_files):
    """
    C: 2020.07.11
    M: 2020.07.12
    """
    exam = []
    sub_id = []
    im_id = []
    modality = []
    im_name = []
    full_pth = []
    
    for p in ixi_files:
        exam_name = p.parent.name
        exam.append(exam_name)
        
        ex = exam_name.split('-')
        sub_id.append(ex[0])
        im_id.append(ex[2])
        modality.append(ex[3])
        
        im_name.append(p.name)
        full_pth.append(p)
    
        #print(parent, ex, sub_id, im_id, modality, p.name)
        #print(p, p.name)
    df_ixi = pd.DataFrame({'Examination':exam, 'Subject_id':sub_id,'Image_id':im_id,'Modality':modality,
                           'Image':im_name, 'Path':full_pth})
    return df_ixi

def get_aibl_info(aibl_files):
    """
    C: 2020.07.12
    M: 2020.07.12
    """
    exam = []
    sub_id = []
    im_id = []
    modality = []
    im_name = []
    full_pth = []

    for p in aibl_files:
        exam_name = p.parent.name
        exam.append(exam_name)

        ex = exam_name.split('_')
        sub_id.append(ex[-2])
        im_id.append(ex[-1].split('.')[0])
        modality.append('T1.anat')

        im_name.append(p.name)
        full_pth.append(p)

        #print(parent, ex, sub_id, im_id, modality, p.name)
        #print(p, p.name)
    df = pd.DataFrame({'Examination':exam, 'Subject_id':sub_id,'Image_id':im_id,'Modality':modality,
                           'Image':im_name, 'Path':full_pth})
    return df

def get_sald_info(sald_files):
    """
    C: 2020.07.13
    M: 2020.07.13
    """
    exam = []
    sub_id = []
    im_id = []
    modality = []
    im_name = []
    full_pth = []

    for p in sald_files:
        exam_name = p.parent.name
        exam.append(exam_name)

        ex = exam_name.split('_')
        sub_id.append(ex[0])
        im_id.append('')
        modality.append(ex[1])

        im_name.append(p.name)
        full_pth.append(p)

        #print(parent, ex, sub_id, im_id, modality, p.name)
        #print(p, p.name)
    df = pd.DataFrame({'Examination':exam, 'Subject_id':sub_id,'Image_id':im_id,'Modality':modality,
                           'Image':im_name, 'Path':full_pth})
    return df


def get_slim_info(slim_files):
    """
    C: 2020.07.13
    M: 2020.07.13
    """
    exam = []
    sub_id = []
    im_id = []
    modality = []
    im_name = []
    full_pth = []

    for p in slim_files:
        exam_name = p.parent.name
        exam.append(exam_name)

        ex = exam_name.split('_')
        sub_id.append(ex[0])
        im_id.append(ex[1])
        modality.append(ex[2])

        im_name.append(p.name)
        full_pth.append(p)

        #print(parent, ex, sub_id, im_id, modality, p.name)
        #print(p, p.name)
    df = pd.DataFrame({'Examination':exam, 'Subject_id':sub_id,'Image_id':im_id,'Modality':modality,
                           'Image':im_name, 'Path':full_pth})
    return df

def get_hcp_info(hcp_files):
    """
    C: 2020.07.27
    M: 2020.07.27
    """
    exam = []
    sub_id = []
    im_id = []
    modality = []
    im_name = []
    full_pth = []

    for p in hcp_files:
        exam_name = p.parent.name
        exam.append(exam_name)

        ex = exam_name.split('_')
        sub_id.append(ex[0])
        im_id.append('')
        modality.append(ex[-1])

        im_name.append(p.name)
        full_pth.append(p)

        #print(parent, ex, sub_id, im_id, modality, p.name)
        #print(p, p.name)
    df = pd.DataFrame({'Examination':exam, 'Subject_id':sub_id,'Image_id':im_id,'Modality':modality,
                           'Image':im_name, 'Path':full_pth})

    return df


def get_img_params(files_list):
    """
    C: 2020.07.12
    M: 2020.07.12
    """
    shape_l =[]
    dtype_l = []
    max_l = []
    min_l = []
    mean_l = []
    pixdim_l = []
    exam_l = []
    im_name = []

    k = 1
    ln = len(files_list)
    
    for i in files_list:        
        exam_name = i.parent.name
        exam_l.append(exam_name)
        
        im_name.append(i.name)

        ### image
        nii = nib.load(str(i))
        pixdim = nii.header['pixdim'][1:4]    

        data = nii.get_fdata()
        shape = data.shape
        dtype = data.dtype
        mx, mn = data.max(), data.min()
        mean = data.mean()

        shape_l.append(shape)
        dtype_l.append(dtype)
        max_l.append(mx)
        min_l.append(mn)
        mean_l.append(mean)
        pixdim_l.append(pixdim)
        
        print(f'{k}/{ln}  {exam_name}   ', end='\r')
        k += 1

    # split pixdim and voxel size tuples into separate lists
    pixdim_1, pixdim_2, pixdim_3 = np.hsplit(np.array(pixdim_l), 3)
    size_1, size_2, size_3 = np.hsplit(np.array(shape_l), 3)

    df = pd.DataFrame({'Examination': exam_l, 'Image':im_name, 'Max':max_l, 'Mean':mean_l, 'Min':min_l,'Dtype':dtype_l,
                        'Size_1' : np.squeeze(size_1),'Size_2' : np.squeeze(size_2),'Size_3' : np.squeeze(size_3),
                        'Pixdim_1' : np.squeeze(pixdim_1),'Pixdim_2' : np.squeeze(pixdim_2),'Pixdim_3' : np.squeeze(pixdim_3)})
    return df