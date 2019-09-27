# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 12:38:30 2019

@author: mlin
"""

import matplotlib.pyplot as plt
from math import sin, cos, tan, radians


def beam(mag, angle, width, color='blue', fill='True'):
    _width=radians(width)
    _angle=radians(angle)
    points=[(0,0)]
    for i in [radians(i) for i in range(0,180)]:
        dx=mag+mag*tan(_width/2)*sin(i)
        dy=mag*tan(_width/2)*cos(i)
        _dx=cos(_angle)*dx+sin(_angle)*dy
        _dy=sin(_angle)*dx-cos(_angle)*dy
        points.append((_dx, _dy))
    points.append((0,0))
    
    axes= plt.gca()
    axes.set(xlim=(-2, 2), ylim=(0, 2))
    if fill:
        plt.fill(*zip(*points),color)
    else:
        plt.plot(*zip(*points),color)
   


plt.figure(num=None, figsize=(8, 4))
for i in range(20,165,5):
    beam(1.7,i,4.7, 'red')

for i in range(27,170,21):
    beam(1.4,i,20,'green')
    
for i in range(30,180,30):
    beam(1.1,i,29, 'blue')

'''
plt.figure(num=None, figsize=(8, 4))
for i in range(20,170,10):
    beam(1.5,i,9.5,'red')
    
for i in range(20,170,10):
    beam(1.3,i,15, 'blue', False)
'''