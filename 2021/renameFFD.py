# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 11:05:49 2021

@author: mlin
"""
oDesktop.ClearMessages("", "", 2)

import os
import sys
import clr
clr.AddReference("System.Windows.Forms")

from System.Windows.Forms import FolderBrowserDialog, DialogResult
dialog = FolderBrowserDialog()
dialog.SelectedPath = 'c:\\'

if dialog.ShowDialog() == DialogResult.OK:
    ffd_directory = dialog.SelectedPath
    AddWarningMessage(ffd_directory)    
else:
    pass


txt_path = os.path.join(ffd_directory, 'exportelement.txt')
with open(txt_path) as f:
    text = f.readlines()
table = {}
for line in text[1:]:
    try:
        source_name, file_name = line.strip().split()
        source_name = source_name.split(':')[0]
        
        old_path = os.path.join(ffd_directory, file_name+'.ffd')
        new_path = os.path.join(ffd_directory, source_name+'.ffd')
        AddWarningMessage('{} => {}'.format(old_path, new_path))
        os.rename(old_path, new_path)
    except:
        pass
AddWarningMessage('Completed')
    
    
    
