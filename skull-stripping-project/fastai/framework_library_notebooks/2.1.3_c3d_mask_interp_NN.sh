#!/usr/bin/env bash

# MMIV-ML
# C: 2020.08.05
# M: 2020.08.09
# Mask interpolation with NN algorithm

DATA1='IXI' 
DATA2='AIBL' 
DATA3='ADNI'
DATA4='PPMI'
DATA5='SALD'
DATA6='SLIM'
DATA7='HCP'
DATA8='CalgaryCampinas'
DATA9='NFBS'

DATA=$DATA9




folder_in="/data-10tb/marek/$DATA/train_data/FSL_outputs/*/"
folder_out="/data-10tb/shared/skull/train-3d-iso/$DATA/"
   
for name_in in `find $folder_in -name "*T1w_brainmask.nii.gz"`; do    
    f=${name_in##*/} # a file name: T1.nii.gz
    f=${f%.nii.gz} # a filename without extention(s): T1
    f=${f}_iso_nn.nii.gz # a file name with a new extenstion
    #echo ${u}
    parent=${name_in%/*} # remove a file name
    parent=${parent##*/} # get the last folder name
    name_out=${folder_out}${parent}_${f}   

    # test line:
    # #### c3d -int 0 T1_biascorr_brain_mask.nii.gz -type short -noround -resample-mm 1.0mmx1.0mmx1.0mm -o yyy.nii.gz
    # -int 0 - means NN interpolation
    
    echo "ssh marek@129.177.233.24 \"[ ! -e "$name_out" ] && /home/marek/c3d -int 0 \"$name_in\" -type short -noround -resample-mm 1.0mmx1.0mmx1.0mm -o \"$name_out\" && echo ${name_out##*/}...done \""
done



# USAGE
# 1. ./2.1.3_c3d_mask_interp_NN.sh > IXI_resample_NN_jobs.txt - to generate a text file with jobs to do
# 2. Copy IXI_resample_jobs.txt to the deskotop of a local computer (prec-7540)
# 3. run: time parallel --jobs 12 < IXI_resample_NN_jobs.txt