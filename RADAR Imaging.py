# -*- coding: utf-8 -*-
"""
Created on Fri May  3 07:32:40 2019

@author: mlin
"""
from numpy import loadtxt, vectorize, reshape, zeros, arange, append
from numpy import array, exp, fft, sqrt, meshgrid
import scipy.constants as const
import matplotlib.pyplot as plt

class RADAR_Image():
    size=0
    
    def __init__(self, freal, fimag):
        dreal=loadtxt(freal, delimiter=',', skiprows=1, )
        dimag=loadtxt(fimag, delimiter=',', skiprows=1, )
        self.freq=1e9*dreal[:,0]
        self.data=vectorize(complex)(dreal[:,1:], dimag[:,1:])
    
    def _compute(self, z0, ape=0.4):
        global size
        step3=zeros((size, size),dtype=complex)
        wavenumber=2*const.pi*self.freq/const.c
        kc=(2*const.pi/ape)*append(arange(0,int(size/2)+1),arange(-int(size/2),0))
        KX, KY=meshgrid(kc,kc)
        
        complex_data=reshape(self.data, (len(self.freq), size, size))
        
        for i, k in enumerate(wavenumber):
            w=array(4*k*k-KX*KX-KY*KY+0j)
            k_all=exp(1j*sqrt(w)*z0)
            step1=fft.fft2(complex_data[i])
            step2=k_all*step1
            step3+=fft.ifft2(step2)
        
        return step3

    def calculate(self, _size, ape, z=arange(0.4,0.6,0.05)):
        global size
        size=_size
        
        result=zeros((size, size), dtype=complex)
        for i in z:
            result+=self._compute(z0=i, ape=ape)
        return abs(result)

Fre='D:/demo_image/re.csv'
Fim='D:/demo_image/im.csv'
RI=RADAR_Image(Fre, Fim)
plt.imshow(RI.calculate(21, 0.35))