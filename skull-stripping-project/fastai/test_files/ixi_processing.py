### Sathiesh's code...
#### 2020.06.28

def process_ixi_xls(xls_path, img_path):
    print('Preprocessing ' + str(xls_path))
    df = pd.read_excel(xls_path)
    duplicate_subject_ids = df[df.duplicated(['IXI_ID'], keep=False)].IXI_ID.unique()
    for subject_id in duplicate_subject_ids:
        age = df.loc[df.IXI_ID == subject_id].AGE.nunique()
        if age != 1: df = df.loc[df.IXI_ID != subject_id]# #Remove duplicates with two different age values
    df = df.drop_duplicates(subset='IXI_ID', keep='first').reset_index(drop=True)
    df['subject_id'] = ['IXI' + str(subject_id).zfill(3) for subject_id in df.IXI_ID.values]
    df = df.rename(columns={'SEX_ID (1=m, 2=f)': 'gender', 'AGE': 'age_at_scan'})
    df = df.replace({'gender': {1:'M', 2:'F'}})
    img_list = glob(str(img_path/'*'/'T1_biascorr.nii.gz'))
    mask_list = glob(str(img_path/'*'/'T1_biascorr_brain_mask.nii.gz'))
    for path in img_list:
        subject_id = path.split('/')[-2].split('-')[0]
        df.loc[df.subject_id == subject_id, 't1_biascorr_path'] = path
    for path in mask_list:
        subject_id = path.split('/')[-2].split('-')[0]
        df.loc[df.subject_id == subject_id, 'brain_mask_path'] = path
    df = df.dropna()
    df = df[['t1_biascorr_path','brain_mask_path', 'subject_id', 'gender', 'age_at_scan']]
    df['above_60_years'] = df.age_at_scan > 60
    os.remove(xls_path)
    return df
