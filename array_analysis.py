# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 19:24:49 2019
@author: mlin

"""
import matplotlib.pyplot as plt
from collections import OrderedDict
import numpy as np
import copy
import scipy.optimize as optimize
import json

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
        
        self.Ntheta=len(theta_range)
        self.Nphi=len(phi_range)
        
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

    def getE(self, theta, phi):
        index=(theta/self._dtheta)*self.Nphi+phi/self._dphi
        return self._EF[int(index),:]
    
    def getGain(self, theta, phi):
        index=(theta/self._dtheta)*self.Nphi+phi/self._dphi
        return self.realized_gain[int(index)]
        
    def shiftPhase(self, angle):
        x=copy.deepcopy(self)
        x._EF=x._EF*np.exp(1j*np.radians(angle))
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
        
class aggregatebeam():
    def __init__(self, *args):
        self.args=args
        self.max_gain=np.copy(args[0].realized_gain)
        self.beam_occupy=0*np.copy(self.max_gain)
        
        for beamid, i in enumerate(self.args[1:], 1):
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
        return (x, y/y[-1])

    
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

class GainOptimizer():
    def __init__(self, ffds):
        self.ffds=ffds
    
    def _factory(self, theta, phi):
        def weighting(x):
            U, V=0+0j, 0+0j
            for i, j in zip(self.ffds,x):
                U+=i.getE(theta, phi)[0]*np.exp(1j*np.radians(j))
                V+=i.getE(theta, phi)[1]*np.exp(1j*np.radians(j))
            return -np.sqrt(np.power(np.absolute(U),2)+np.power(np.absolute(V),2)) 
        return weighting

    def run(self, resolution=20):
        theta=range(0, 180+resolution, resolution)
        phi=range(0, 360+resolution, resolution)
        initial_guess=[0]*len(self.ffds)
        
        self.phase_table=OrderedDict()    
        self.area_gain=[]
        
        for i in theta:
            for j in phi:
                if (i==0 and j!=0) or (i==180 and j!=0):
                    continue
                
                weighting=self._factory(i, j)
                result= optimize.minimize(weighting, initial_guess)
                
                if result.success:
                    ffdsum=self.ffds[0].shiftPhase(result.x[0])
                    initial_guess=[i%360 for i in result.x]
                    for k, m in zip(self.ffds[1:], result.x[1:]):
                        ffdsum+=k.shiftPhase(m)
                    maxGain=ffdsum.getGain(i,j)    
                    self.phase_table[f'{i},{j}']=([i%360 for i in result.x], maxGain)
                    self.area_gain.append((maxGain, np.sin(np.radians(i))))
                    print(f'{i:4d},{j:4d}: {maxGain:.3f}(dB)')
                    print(result.x)
                else:
                    self.phase_table[(i,j)]='Optimization Failed'
                    
    def saveJSON(self, file):
        with open(file, 'w') as f:
            json.dump(self.phase_table, f, indent=2)
    
    def plotOptimalCDF(self):
        A=0
        x, y=[], []

        for i,j in sorted(self.area_gain):
            x.append(i)
            A+=j
            y.append(A)
        y=[i/y[-1] for i in y]
        plt.figure()
        plt.title('Optimal CDF')        
        plt.xlabel('Realized Gain (dB)')
        plt.ylabel('CDF')
        plt.grid(True)
        plt.plot(x, y)
        plt.show()
        return (x, y)


def plotCDFtable(table, png=None):
    '''table={'A':(gain , cdf), 'B':(gain, cdf), }'''
    
    plt.figure()
    plt.title('Cumulative Distribution Function')        
    plt.xlabel('Realized Gain (dB)')
    plt.ylabel('CDF')
    plt.grid(True)
    for i in table:
        plt.plot(*table[i], label=i)
    plt.legend()
    if png:
        plt.savefig(png)    
    plt.show()
#%%


path='D:/demo3/28000000000'
x1=ffd(path+'/Module_0_Bump_h1.ffd')
x2=ffd(path+'/Module_0_Bump_h2.ffd')
x3=ffd(path+'/Module_0_Bump_h3.ffd')
x4=ffd(path+'/Module_0_Bump_h4.ffd')

pt=GainOptimizer([x1, x2, x3, x4])
pt.run(10)
pt.saveJSON(path+'/phase.json')
#%%
table={}
table['optimal']=pt.plotOptimalCDF()
plotCDFtable(table)
#%%

beam0=x1(1,0) +x2(1,0) +x3(1,0) +x4(1,0)
beam0.plotRealizedGain()
beam1=x1(1,0) +x2(1,60) +x3(1,120) +x4(1,180)
beam1.plotRealizedGain()
beam2=x1(1,0) +x2(1,120) +x3(1,240) +x4(1,360)
beam2.plotRealizedGain()
beam3=x1(1,0) +x2(1,-60) +x3(1,-120) +x4(1,-180)
beam3.plotRealizedGain()
beam4=x1(1,0) +x2(1,-120) +x3(1,-240) +x4(1,-360)
beam4.plotRealizedGain()

z0=aggregatebeam(beam0)
table['0']=z0.plotCDF()
z1=aggregatebeam(beam1)
table['1']=z1.plotCDF()
z2=aggregatebeam(beam2)
table['2']=z2.plotCDF()
z3=aggregatebeam(beam3)
table['3']=z3.plotCDF()
z4=aggregatebeam(beam4)
table['4']=z4.plotCDF()
z01234=aggregatebeam(beam0, beam1, beam2,beam3,beam4)
#%%
table['01234']=z01234.plotCDF()
plotCDFtable(table)
z01234.plotGainMap()
z01234.plotBeamMap()