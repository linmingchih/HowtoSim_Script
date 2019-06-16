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
        plt.figure(figsize=(8, 4))
        size=(self.theta[2], self.phi[2])
        gain_map=self.realized_gain.reshape(size)
        plt.title('Map of Realized Gain(dB)')
        plt.xlabel('Phi (degree)')
        plt.ylabel('Theta (degree)')
        maxV=np.max(gain_map)
        [row, col] = np.where(gain_map==maxV)
        plt.plot(col, row, 'w*')
        plt.annotate(round(maxV,3), (col+3, row+3), color='white')
        plt.imshow(gain_map, cmap='jet')
        plt.colorbar()
        CS=plt.contour(gain_map)        
        plt.clabel(CS, inline=1, fontsize=10)
        
class aggregateffd():
    def __init__(self, *args):
        self.args=args
        self.max_gain=args[0].realized_gain
        self.beam_occupy=0*self.max_gain
        
        for beamid, i in enumerate(args[1:], 1):
            for n in range(len(self.max_gain)):
                if i.realized_gain[n]>self.max_gain[n]:
                    self.beam_occupy[n]=beamid
                    self.max_gain[n]=i.realized_gain[n]

        self.map_size=(args[0].theta[2], args[0].phi[2])

    
    def plotCDF(self):
        x, y=[], []
        accumulated_area=0
        for gain, area in sorted(zip(self.max_gain, self.args[0].cell_area)):
            x.append(gain)
            accumulated_area+=area
            y.append(accumulated_area)
        
        plt.figure()
        plt.title('Cumulative Distribution Function')        
        plt.xlabel('Realized Gain (dB)')
        plt.ylabel('CDF')
        plt.grid(True)
        plt.plot(x, y/y[-1])
        plt.show()

    
    def plotGainMap(self):
        gain_map=self.max_gain.reshape(self.map_size)
        
        plt.figure(figsize=(8, 4))
        plt.title('Gain Map(dB)')
        plt.xlabel('Phi (degree)')
        plt.ylabel('Theta (degree)')
        maxV=np.max(gain_map)
        [row, col] = np.where(gain_map==maxV)
        plt.plot(col, row, 'w*')
        plt.annotate(round(maxV,3), (col+3, row+3), color='white')
        plt.imshow(gain_map, cmap='jet')
        plt.colorbar()
        CS=plt.contour(gain_map)
        plt.clabel(CS, inline=1, fontsize=10)        

    
    def plotBeamMap(self):
        beam_map=self.beam_occupy.reshape(self.map_size)
        
        plt.figure(figsize=(8, 4))
        plt.title('Beam Map')        
        plt.xlabel('Phi (degree)')
        plt.ylabel('Theta (degree)')        
        plt.imshow(beam_map, cmap='rainbow')
        plt.colorbar()        
        plt.contour(beam_map)


#%%

x1=ffd('D:/demo5/28000000000/1.ffd')
x2=ffd('D:/demo5/28000000000/2.ffd')
x3=ffd('D:/demo5/28000000000/3.ffd')
x4=ffd('D:/demo5/28000000000/4.ffd')
x5=ffd('D:/demo5/28000000000/5.ffd')
x6=ffd('D:/demo5/28000000000/6.ffd')
x7=ffd('D:/demo5/28000000000/7.ffd')
x8=ffd('D:/demo5/28000000000/8.ffd')

#%%

y0=x1(1,0) +x3(1,0) +x5(1,0) +x7(1,0)
y0.plotRealizedGain()
y1=x1(1,0) +x3(1,75) +x5(1,150) +x7(1,225)
y1.plotRealizedGain()
y2=x1(1,0) +x3(1,150) +x5(1,300) +x7(1,450)
y2.plotRealizedGain()

#%%
z=aggregateffd(y0, y1, y2)
z.plotCDF()
z.plotBeamMap()
z.plotGainMap()
