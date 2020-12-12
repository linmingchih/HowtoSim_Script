# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 12:08:38 2020

@author: mlin
"""
import math, os, sys, re
import webbrowser
import matplotlib.pyplot as plt

def RI(x, y):
    z = abs(complex(x, y))
    if z <= 0:
        z = sys.float_info.min
    return 20*math.log10(z)

def DB(x):
    return x

def MA(x):
    if x <= 0:
        x = sys.float_info.min
    return 20*math.log10(x)

model = []
touchstone = sys.argv[1]
ts_dir = os.path.dirname(touchstone)
ts_basename = os.path.basename(touchstone).split('.')[-2]
Nport = int(touchstone.split('.')[-1][1:-1])

unit_mapping = {'HZ':1e0, 'KHZ':1e3, 'MHZ':1e6, 'GHZ':1e9}
data = []
port_dict = {}
with open(touchstone) as f:
    for i in f:
        if i[0] =='!':
            try:
                m = re.search('Port\[(\d+)\]\s=\s(\S+)', i)
                port_dict[int(m.group(1))] = m.group(2)
            except:
                pass
        elif i[0] == '#':
            _, freq_unit, mtype, mformat, _, _ = i.strip().split()
            scale = unit_mapping[freq_unit.upper()]
            if mtype != 'S':
                raise Exception("Can't handle {} matrix".format(mtype))
        else:
            model += [float(v) for v in i.strip().split()]
        
        if len(model) > 2*Nport*Nport+1:
            x = model[1:2*Nport*Nport+1]
            break


            
mformat = mformat.upper()

if mformat == 'RI':
    data = [RI(i, j) for i, j in zip(x[0::2], x[1::2])]
elif mformat == 'DB':
    data = [DB(i) for i in x[0::2]]
elif mformat == 'MA':
    data = [MA(i) for i in x[0::2]]
    
matrix = []
for i in range(Nport):
    matrix.append(data[i*Nport:(i+1)*Nport])

pair = []    
for m, i in enumerate(matrix):
    n, v = max(enumerate(i), key=lambda item:item[1])
    pair.append((m,n))

images = []

outputdir = os.path.join(ts_dir,ts_basename)
try:                             
    os.mkdir(outputdir)
except:
    pass

text = [] 
with open(touchstone) as f:
    for i in f:
        if i[0] in ['!', '#']:
            continue
        else:
            text += i.strip().split()

freq = [float(i)*scale/1e9 for i in text[0::Nport*Nport*2+1]]
            
for m, n, in pair:
    color = 'b' if m!=n else 'r'
    if mformat == 'RI':
        x = zip(text[(m*Nport+n)*2+1::Nport*Nport*2+1],
                text[(m*Nport+n)*2+2::Nport*Nport*2+1])
        y = [RI(float(i), float(j)) for i, j in x]
    elif mformat == 'DB':
        y = [DB(float(i)) for i in text[(m*Nport+n)*2+1::Nport*Nport*2+1]]
    elif mformat == 'MA':
        y = [MA(float(i)) for i in text[(m*Nport+n)*2+1::Nport*Nport*2+1]]
        
    plt.figure(figsize=(6,4))    
    plt.clf()
    axes = plt.gca()
    plt.gca().set_xlim(0, freq[-1])
    plt.gca().set_ylim(min(y), 0)
    plt.grid()
    plt.xlabel('Frequency[GHZ]')
    plt.ylabel('Magnitude[DB]')
    plt.plot(freq, y, color)
    if len(port_dict) == Nport:
        plt.title(f'S({port_dict[m+1]}, {port_dict[n+1]})')
    else:
        plt.title(f'S({m+1},{n+1})')
    imagename = f'{outputdir}/{m+1}_{n+1}.png'
    plt.savefig(imagename)
    images.append(imagename)



x1 = '<tr><td><img src={}></td><td><img src={}></td><td><img src={}></td><td><img src={}></td></tr>\n'
div = (len(images)//4)
mod = (len(images)%4)
x2 = x1 * div if mod == 0 else x1*(div + 1)
x3 = images + [''] * mod
x4 = x2.format(*[i.replace(' ', '%20') for i in x3])
html1 = '''<H1>Insertion Loss</H1>
    <table >
{}
    </table>
'''.format(x4)


if port_dict:
    x5 = ''
    for m, n in pair:
        x5 += f'<tr><td><font size="4">S({m+1},{n+1})</font></td><td><font size="4">{m+1}:{port_dict[m+1]}</font></td><td><font size="4">{n+1}:{port_dict[n+1]}</font></td></tr>\n'
    
    html2 = '''<H1>Port Pair</H1>
        <table border="1" cellpadding="10" cellspacing="0.1">
    {}
        </table>
    '''.format(x5)
else:
    html2 = ''
    
html_path = os.path.join(ts_dir, ts_basename+'.html')
with open(html_path, 'w') as f:
    f.write(html1 + html2)
webbrowser.open(html_path)