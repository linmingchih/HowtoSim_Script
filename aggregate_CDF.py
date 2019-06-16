# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 19:24:49 2019

@author: mlin
"""
import matplotlib.pyplot as plt
import numpy as np
import copy

class ffd():    
    def __init__(self, ffd_file, incident_Power_W=1):
        self.incident_Power_W=incident_Power_W
        
        with open(ffd_file) as f:
            self.theta=[int(i) for i in f.readline().split()] 
            self.phi=[int(i) for i in f.readline().split()]
            f.readline()
            self.frequency=float(f.readline().split()[1])
        
        theta_range=np.linspace(*self.theta)
        phi_range= np.linspace(*self.phi)
        
        self._dtheta=theta_range[1]-theta_range[0]
        self._dphi=phi_range[1]-phi_range[0]
        self._theta=np.array([i for i in theta_range for j in phi_range])        
        
        EF=np.loadtxt(ffd_file, skiprows=4)
        
        Etheta=np.vectorize(complex)(EF[:,0], EF[:,1])
        Ephi=np.vectorize(complex)(EF[:,2], EF[:,3])
        self._EF=np.column_stack((Etheta, Ephi))        
        self._calculate()
        
    def __eq__(self, other):
        if self.theta!=other.theta:
            return False        
        if self.phi!=other.phi:
            return False        
        if self.frequency!=other.frequency:
            return False        
        return True
    
    def __add__(self, other):
        if self==other:
            x=copy.deepcopy(self)
            x._EF+=other._EF
            x.incident_Power_W+=other.incident_Power_W
            x._calculate()            
            return x
        
    def _calculate(self):
        pd=np.sum(np.power(np.absolute(self._EF), 2),1)/377/2
        self.U=max(pd)
        self.cell_area=np.radians(self._dtheta)*np.radians(self._dphi)*np.sin(np.radians(self._theta))
        #self.radiated_power=sum(self.cell_area*pd)
        #uniform_power=self.radiated_power/sum(self.cell_area)
        #self.peak_directivity=self.U/uniform_power
        
        self.realized_gain=10*np.log10(pd/(self.incident_Power_W/4/np.pi))
        self.peak_realized_gain=max(self.realized_gain)

    def compare(self, other):
        x=np.abs(self._EF)
        dx=np.abs(other._EF-self._EF)
        return np.amax(dx/x)    
     
    def __call__(self, mag, phase):
        x=copy.deepcopy(self)
        x._EF=np.sqrt(mag)*np.exp(1j*np.radians(phase))*self._EF
        x.incident_Power_W=mag
        x._calculate()
        return x    
    
    def getCDF(self):
        x, y=[], []
        accumulated_area=0
        for gain, area in sorted(zip(self.realized_gain, self.cell_area)):
            x.append(gain)
            accumulated_area+=area
            y.append(accumulated_area)
        return x, y/y[-1]
    
    def plotRealizedGain(self):
        plt.figure()
        size=(self.theta[2], self.phi[2])
        gain_map=self.realized_gain.reshape(size)
        plt.xlabel('Phi (degree)')
        plt.ylabel('Theta (degree)')

        plt.imshow(gain_map, cmap='rainbow')
        plt.colorbar()
        

def aggregateffd(*args):
    max_gain=args[0].realized_gain
    beam_occupy=0*args[0].realized_gain
    for beamid, i in enumerate(args[1:], 1):
        for n in range(len(max_gain)):
            if i.realized_gain[n]>max_gain[n]:
                beam_occupy[n]=beamid
                max_gain[n]=i.realized_gain[n]

    x, y=[], []
    accumulated_area=0
    for gain, area in sorted(zip(max_gain, args[0].cell_area)):
        x.append(gain)
        accumulated_area+=area
        y.append(accumulated_area)
    
    map_size=(args[0].theta[2], args[0].phi[2])
    return (x, y/y[-1]), max_gain.reshape(map_size), beam_occupy.reshape(map_size)

#%%

x1=ffd('d:/demo3/ant1.ffd')
x2=ffd('d:/demo3/ant2.ffd')
x3=x1(2,20)+x2(5,90)
print(x3.peak_realized_gain)

gain=[]
for i in range(360):
    x3=x1+x2(1,i)
    gain.append(x3.peak_realized_gain)
    
plt.figure()
plt.plot(gain)
plt.show()
