#!/usr/bin/env bash

# MMIV-ML
# C: 2020.07.09
# M: 2020.08.09

# Convert all data {T1, T1_biascorr, masks} to isotropic images.
# This file should be updated to use different interpolation methods:
# 1. linear - for T1 and T1_biascorr (to be compatybile with interpolatin used in Monai library)
# 2. neares neighbour for masks


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

#ls $folder_in

for u in `find $folder_in -name "*T1w.nii.gz"`; do
	f=${u##*/} # a file name: T1.nii.gz
	f=${f%.nii.gz} # a filename without extention(s): T1
	f=${f}_iso.nii.gz # a file name with a new extenstion
	#echo ${u}
	parent=${u%/*} # remove a file name
	parent=${parent##*/} # get the last folder name
	name_out=${folder_out}${parent}_${f}
    
    # local - dry-run
	#echo ${name_out}    
    
    # convertion: c3d software
    # exmple: run on Titan FROM a local computer 
    # dry-run or to pipeline to a txt or sh file
    # to run: copy pipelined file to a local computer and run it
    
    # TO CHECK in the future (!):
    # 1) c3d input.img -interpolation Cubic -resample 50x30x40vox -o output.img
    # 2) c3d -int 0 T1_biascorr_brain_mask.nii.gz -type short -noround -resample-mm 1.0mmx1.0mmx1.0mm -o yyy.nii.gz
    
    
    echo "ssh marek@129.177.233.24 \"[ ! -e "$name_out" ] && /home/marek/c3d \"$u\" -resample-mm 1.0mmx1.0mmx1.0mm -o \"$name_out\" && echo ${name_out##*/}...done \""
    
    

    # to progress display
    #echo "echo ${name_out##*/}...done"
done


# USAGE
# 1. ./2.1_c3d_convert_to_iso.sh > IXI_resample_jobs.txt - to generate a text file with jobs to do
# 2. Copy IXI_resample_jobs.txt to the deskotop of a local computer (prec-7540)
# 3. run: time parallel --jobs 24 < IXI_resample_jobs.txt


# try from a local computer on a server (for one file in the home directory)
#ssh marek@129.177.233.24 /home/marek/c3d T1.nii.gz -resample-mm 1.0mmx1.0mmx1.0mm -o T1_iso.nii.gz # 
