# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 10:25:14 2019

@author: mlin
"""
import re, collections
import matplotlib.pyplot as plt
import webbrowser, os

def readMatrix(file):
    with open(file) as f:
        text=f.readlines()
    
    header=re.findall(r'\"(.+?)\"', text[0])
    
    data=[]
    for i in text[1:]:
        data.append([float(j) for j in i.split(',')])
    
    data=list(map(list, zip(*data)))   
    
    result=collections.OrderedDict()
    
    for i in range(len(header)):
        result[header[i]]=data[i]
    
    return result

def genCompare(f1, f2, html_file):
    data1=readMatrix(f1)
    data2=readMatrix(f2)
    gallery=[]

    for k, i in enumerate(data1):
        plt.clf()
        if i=='Freq [GHz]': continue
        try:
            plt.plot(data1['Freq [GHz]'], data1[i],'bo')
            plt.plot(data2['Freq [GHz]'], data2[i],'rx')
        except:
            print('Failed:'+i)
            continue            
        
        plt.ylabel(i)
        plt.xlabel('Freq [GHz]')         
        path='d:/demo/{}.png'.format(k)
        plt.savefig(path, dpi=300)
        gallery.append(path)

        
    with open(html_file, 'w') as f:            
        for k in gallery:
            f.writelines('<img src="{}">\n'.format(k))
                
    webbrowser.open('file://' + os.path.realpath(html_file))          
        
f1='d:/demo/db1.csv' 
f2='d:/demo/db2.csv'    
genCompare(f1, f2, 'd:/demo/compare.html')







