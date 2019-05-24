# -*- coding: utf-8 -*-
"""
Created on Tue May 21 16:22:46 2019

@author: mlin
"""

import os, subprocess
import xml.etree.cElementTree as ET

aedt_path='C:/Program Files/AnsysEM/AnsysEM19.4/Win64'

class net():
    def __init__(self, xmlfile):
        ET.register_namespace('c', "http://www.ansys.com/EDBBuilderUtils/SetupInfo")
        self.tree = ET.ElementTree(file=xmlfile)
        self.dir=os.path.dirname(xmlfile)
        self.reset()
        
    def reset(self):
        for elem in self.tree.iter(tag='Net'):
            elem.attrib['Import']="False"
            try:
                del(elem.attrib['PinsBecomePorts'])
            except:
                pass
            try:
                del(elem.attrib['Class'])
            except:
                pass
            try:
                del(elem.attrib['Floating'])
            except:
                pass
        return self
    
    def setPort(self, nets):        
        for elem in self.tree.iter(tag='Net'):
            if elem.attrib['Name'] in nets: 
                elem.attrib['Import']="True"
                elem.attrib['PinsBecomePorts']="True"
        return self
                
    def setGround(self, nets):
        for elem in self.tree.iter(tag='Net'):
            if elem.attrib['Name'] in nets:
                elem.attrib['Import']="True"
                elem.attrib['Class']="Power/Ground"
        return self
            
    def setFloating(self, nets):
        for elem in self.tree.iter(tag='Net'):
            if elem.attrib['Name'] in nets:
                elem.attrib['Import']="True"                
                elem.attrib['Class']="Power/Ground"
                elem.attrib['Floating']="True"
        return self
    
    def save_aedb(self, name):
        wk_dir=f'{self.dir}/{name}'
        self.xml=f'{wk_dir}/{name}.xml'
        self.aedb=f'{wk_dir}/{name}.aedb'
        
        try:
            os.mkdir(wk_dir)
        except:
            pass

        self.tree.write(self.xml, encoding='utf-8', xml_declaration=True)
        cmd=[f'{aedt_path}/PinToPinSetup.exe', wk_dir, self.xml, self.aedb]
        p=subprocess.Popen(cmd)
        p.wait()
        return self
       
    def runBatch(self):
        cmd=[f'{aedt_path}/ansysedt.exe', '-ng', '-monitor', '-batchsolve', self.aedb]
        p=subprocess.Popen(cmd)
        p.wait()

# =============================================================================
# Set Nets to Extract:
# =============================================================================

ddr4_nets={}
ddr4_nets['BYTE_0']=[f'DDR4_DQ{i}' for i in range(0,8)]
ddr4_nets['BYTE_1']=[f'DDR4_DQ{i}' for i in range(8,16)]
#ddr4_nets['BYTE_2']=[f'DDR4_DQ{i}' for i in range(16,24)]
#ddr4_nets['BYTE_3']=[f'DDR4_DQ{i}' for i in range(24,32)]

pcie_nets={}
pcie_nets['lane_0']=["PCIE_TX0_P","PCIE_TX0_N", "PCIE_RX0_P","PCIE_RX0_N"]
pcie_nets['lane_1']=["PCIE_TX1_P","PCIE_TX1_N", "PCIE_RX1_P","PCIE_RX1_N"]
#pcie_nets['lane_2']=["PCIE_TX2_P","PCIE_TX2_N", "PCIE_RX2_P","PCIE_RX2_N"]
#pcie_nets['lane_3']=["PCIE_TX3_P","PCIE_TX3_N", "PCIE_RX3_P","PCIE_RX3_N"]
#pcie_nets['lane_4']=["PCIE_TX4_P","PCIE_TX4_N", "PCIE_RX4_P","PCIE_RX4_N"]
#pcie_nets['lane_5']=["PCIE_TX5_P","PCIE_TX5_N", "PCIE_RX5_P","PCIE_RX5_N"]
#pcie_nets['lane_6']=["PCIE_TX6_P","PCIE_TX6_N", "PCIE_RX6_P","PCIE_RX6_N"]
#pcie_nets['lane_7']=["PCIE_TX7_P","PCIE_TX7_N", "PCIE_RX7_P","PCIE_RX7_N"]

queue=[]

for byte in ddr4_nets:
    x=net('d:/demo2/ddr4.xml')
    x.setPort(ddr4_nets[byte])
    x.setGround(['GND'])
    x.save_aedb(byte)
    queue.append(x)
    
for lane in pcie_nets:
    x=net('d:/demo2/pcie.xml')
    x.setPort(pcie_nets[lane])
    x.setGround(['GND'])
    x.save_aedb(lane)
    queue.append(x)

for i in queue:
    i.runBatch()