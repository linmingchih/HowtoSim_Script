# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 14:12:49 2019

@author: mlin
"""
import numpy as np

import math
import matplotlib.pyplot as plt

class ffd_CDF():
    def __init__(self, ffd_file):
        self._read(ffd_file)
        self._compute()
    
    def _read(self, ffd_file):
        with open(ffd_file) as f:
            text=f.readlines()

        t=[int(i) for i in text[0].split(' ')]
        p=[int(i) for i in text[1].split(' ')]
        
        convert=lambda x:math.pi*(x/180)
        
        self.dtheta=convert((t[1]-t[0])/(t[2]-1))
        self.dphi=convert((p[1]-p[0])/(p[2]-1))
        theta=[convert(t[0])+i*self.dtheta for i in range(t[2])]
        phi=[convert(p[0])+i*self.dphi for i in range(p[2])]
        
        E=[]        
        for i in text[4:]:
            E.append([float(j) for j in i.strip().split(' ')])

        self.fld=zip(self._duplicate(theta, len(phi)), phi*len(theta),E)
    
    def _duplicate(self, x_list, y):
        result=[]
        for i in x_list:
            for j in range(y):
                result.append(i)
        return result
    
    def _compute(self):
        data=[]
        Etotal, stotal=0, 0
        Esum=0
        for theta, phi, E in self.fld:
            Esum=math.sqrt(sum([i*i for i in E]))
            ds=abs(self.dtheta*self.dphi*math.sin(theta))
            stotal+=ds
            Etotal+=Esum#*ds
            data.append((ds,Esum))
        
        x, y = [], []
        z=0
        Eaverage=Etotal/len(data)#/stotal
        data_n=[(Esum/Eaverage, ds/stotal) for ds, Esum in data]
        data_n.sort()
    
        for i , j in data_n:        
            x.append(10*math.log(i))
            z+=j
            y.append(z)
        
        self.CDF=list(zip(x,y))        
    
    def plot(self):
        x,y=zip(*self.CDF)
        plt.plot(x,y)
        plt.grid(True)
        plt.yticks(np.arange(0, 1.1, 0.1))
        plt.xticks(np.arange(-40, 10, 5))
        plt.show()
    
    def save(self):
        return self.CDF
    
cdf1=ffd_CDF('D:/Customer2019/2019_4_12_5G_CDF/exportfields.ffd')
cdf1.plot()



