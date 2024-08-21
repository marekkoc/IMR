#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 11:46:01 2020
@author: marek

C: 2020.05.11
M: 2020.05.11
"""

import os
import shutil

pth1 = '/data-10tb/marek/AIBL/train_data/FSL_outputs'
fsave = '/data-10tb/marek/AIBL/train_data/FSL_outputs/AIBL_without_mask.txt'
os.chdir(pth1)

folders = os.listdir('.')
folders = [f for f in folders if os.path.isdir(f)]
print(len(folders))

file1 = open(fsave, "a") 

for k, f in enumerate(folders):
    files = os.listdir(f)
    filesNr = len(files)
    if filesNr != 3:
        print(k, filesNr, files, f)
        file1.write(30*'*')
        file1.write('\n')
        file1.write(f)
        file1.write('\n')
        for fl in files:
            file1.write(fl)
            file1.write('\n')
        ### UWAGA: 
        ### KASOWANIE KATALOGOW
        ### ODKOMENTOWAC !!!!
        # shutil.rmtree(f)

file1.close()
