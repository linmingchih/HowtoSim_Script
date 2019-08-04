# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 13:36:30 2019

@author: mlin
"""
import re
from collections import OrderedDict
import numpy as np

def read_Q3D_matrix(matlab_file):
    with open(matlab_file) as f:
        text=' '.join([i.strip() for i in f.readlines()])
    
    m=re.findall('(\w+) = \[(.*?)\]', text)
    
    matrix=OrderedDict()
    for k, data in m:
        x=[]
        for i in data.split(';'):
            try:
                x.append([float(j.strip()) for j in i.split(',')])
            except:
                pass
        matrix[k]=np.array(x)
    return matrix
    
matrix=read_Q3D_matrix('d:/demo/Project4_Q3DDesign1.m')
x=matrix['capMatrix']
y=np.zeros(x.shape)
for m in range(x.shape[0]):
    for n in range(x.shape[1]):
        y[m][n]=abs(x[m][n])/np.sqrt(x[m][m]*x[n][n])

print(y)
print(matrix['capMatrixCoupling'])