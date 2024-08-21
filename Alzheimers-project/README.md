**Source** folder (**src**) contains both Jupyter notebook and mci_modules. Notebooks are named accoring with their task. With some of them acompanion Python modules (with encapsulate auxiliary functions) are linked. A flow charts of selected notebook pipelines are placed in the *figs* folder.

---
## DATA PREPARATION PREPROCESSING AND EXTERNAL TABLES LINKING

**2.01-data2-preprocessin-linking.ipynb**  - The main framework file from `adnimerge.csv`load to save `long.csv` and `bl.csv`  files. Its flow chart is in figs floder. The script contains the following steps:

- feature selection,
- linking with external tables,
- train / test set splitting with data balancing,
- saving results to folder results/20201110
 	


**2.02-data2-descriptive-balance-check.ipynb** - process of split the whole data between `train` and `test` sets including data balance according to Age, Subgroup and Gender.

**2.03-data2-descriptive-long-train-test.ipynb** - statistical description of data sets

**2.04-data2-descriptive-freesurfer.ipynb** - selected features from FreeSurefer are compared between long and cross pahts and visually presented.


---
## LINEAR MIXED EFFECT MODELS  


**2.11-data2-descriptive-LMEM-cros-long.ipynb** - Linear Mixed Effect Models for longitudinal data.


---
## RANDOM FORESTS  - LONGITUDINAL


2.21-data2-RF-long.ipynb

---
## RANODM FORESTS - BASELINE 


2.31-data2-RF-GS-bl - 

2.32-data2-RF-bl - RF with randomly selected parameters. The whole paht is presented.

 

 
---
## MCI MODULES
- mci_balancing.py
- mci_freesurfer.py
- mci_get.py
- mci_info.py
- mci_linking.py
- mci_lmem.py
- mci_plot.py
- mci_preprocessing.py
- mci_utils.py

---
## Folders:

- **assets**   - older version scriptes, test files etc
- **Ingrid** -  base line files

---
Created 2020.12.02 / Updated 2021.04.26

---
