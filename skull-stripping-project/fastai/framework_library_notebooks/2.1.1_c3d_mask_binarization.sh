#!/usr/bin/env bash

# MMIV-ML
# C: 2020.07.09
# M: 2020.07.10
# Mask binarization after resampling.


# QUESTION:
# BINARISATION OR THRESHODLING? WHAT THRESH VALUE? IT CAN HAVE INFLUENCE ON MASK SIZE
# Binarisaation probably increases mask size.



DATA1='IXI' 
DATA2='AIBL' 
DATA3='ADNI'
DATA4='PPMI'
DATA5='SALD'
DATA6='SLIM'
DATA7='HCP'

DATA=$DATA2

#ls $folder_in


#for DT in $DATA1 $DATA2 $DATA3 $DATA4 $DATA5 $DATA6 $DATA7
for DT in $DATA2 $DATA7
do
    DATA=$DT
    folder="/data-10tb/shared/skull/train-3d-iso/$DATA/"
    #echo $folder    
        for u in `find $folder -name "*_brain_mask_iso.nii.gz"`; do            
            /home/marek/c3d ${u} -binarize -type short -o ${u}
            echo $u
        done
done