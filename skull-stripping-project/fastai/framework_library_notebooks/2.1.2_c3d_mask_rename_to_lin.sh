#!/usr/bin/env bash

# MMIV-ML
# C: 2020.08.05
# M: 2020.08.05
#
# Add to the all existing mask suffix *_lin*. As the previous interpolation method is Linear.
# The new interpolation method is NN, is done in the next step (2.1.3) with naming convention *_iso_nn.nii.gz


DATA1='IXI' 
DATA2='AIBL' 
DATA3='ADNI'
DATA4='PPMI'
DATA5='SALD'
DATA6='SLIM'
DATA7='HCP'

DATA=$DATA1

#ls $folder_in


#for DT in $DATA1 $DATA2 $DATA3 $DATA4 $DATA5 $DATA6 $DATA7
for DT in $DATA
do
    DATA=$DT
    folder="/data-10tb/shared/skull/train-3d-iso/$DATA/"
    #echo $folder    
        for u in `find $folder -name "*_brain_mask_iso.nii.gz"`; do      
            f=${u%.nii.gz} # a filename without extention(s): T1
            f=${f}_lin.nii.gz # a file name with a new extenstion
            mv ${u} ${f}
            echo "$u --> $f"
        done
done