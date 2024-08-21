 #!/usr/bin/env bash

# MMIV-ML
# C: 2020.04.30
# M: 2020.07.27

DATA1='IXI' 
DATA2='AIBL' 
DATA3='ADNI'
DATA4='PPMI'
DATA5='SALD'
DATA6='SLIM'
DATA7='HCP-WU-Minn'
DATA8='CalgaryCampinas'

DATA=${DATA8}

### UWAZAC NA source - ORYGINALY!!!
source="/data-nas/brains/${DATA}/FSL_outputs/"


destination="/data-10tb/marek/${DATA}/train_data/FSL_outputs"

### destination NOT source!!!!!
if [ -d ${destination} ]
then
    echo "${DATA} Directory already exists"
else
### destination NOT source!!!!!    
    mkdir -p ${destination}
fi



### DRY-RUN:
#rsync -avm --dry-run --filter="merge 1.0_filter.txt" ${source}sub-25632* ${destination}

### RUN:
rsync -avm --filter="merge 0.1_filter.txt" ${source} ${destination}


# Remark:
# HCP-WU-Minn manually renamed do HCP (!)