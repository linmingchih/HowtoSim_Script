
from numpy import vectorize, reshape, zeros, arange, append, array
from numpy import array, exp, fft, sqrt, meshgrid
import scipy.constants as const
import matplotlib.pyplot as plt

def loadtxt(csv_path):
    freq = {}
    with open(csv_path) as f:
        text = f.readlines()
        for line in text[1:]:
            try:
                _, _, f, value = line.strip().split(',')
            
                if float(f) not in freq:
                    freq[float(f)] = [float(value)]
                else:
                    freq[float(f)] += [float(value)]
            except:
                pass
            
    result = []
    for f, values in freq.items():
        result += values
    
    return array(list(freq.keys())), array(result)
            
x = loadtxt('D:/demo/re.csv')           


class RADAR_Image():
    size=0
    
    def __init__(self, freal, fimag):
        freq, dreal=loadtxt(freal)
        freq, dimag=loadtxt(fimag)
        self.freq = freq*1e9
        self.data=vectorize(complex)(dreal, dimag)
    
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

Fre='D:/demo/re.csv'
Fim='D:/demo/im.csv'
RI=RADAR_Image(Fre, Fim)
plt.imshow(RI.calculate(21, 0.35))
