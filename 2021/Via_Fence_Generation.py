# coding=UTF-8
distance = 20
gap = 30

import os, sys, re, math, json, time, clr, logging
from math import sin, cos, atan, pi, sqrt, acos, degrees

os.chdir(os.path.dirname(__file__))
t0 = time.time()


import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oDesktop.ClearMessages("", "", 2)
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.GetActiveEditor()
unit = oEditor.GetActiveUnits()

def duplicateNewVia(via_name, x, y):
    x0 = oEditor.FindObjects('type', 'via')
    newvia = oEditor.Duplicate(
        [
            "NAME:options",
            "count:="		, 1
        ], 
        [
            "NAME:elements", 
            via_name
        ], [0, 0])
    x1 = oEditor.FindObjects('type', 'via')    
    newvia = list(set(x1).difference(set(x0)))[0]
    
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:BaseElementTab",
                [
                    "NAME:PropServers", 
                    newvia
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Location",
                        "X:="			, "{}{}".format(x, unit),
                        "Y:="			, "{}{}".format(y, unit)
                    ]
                ]
            ]
        ])

def getAngle(v1, v2):
    v1_mag = sqrt(v1[0]**2 + v1[1]**2)
    v2_mag = sqrt(v2[0]**2 + v2[1]**2)
    dotsum = v1[0]*v2[0] + v1[1]*v2[1]
    if v1[0]*v2[1] - v1[1]*v2[0] > 0:
        scale = 1
    else:
        scale = -1
    dtheta = scale*acos(dotsum/(v1_mag*v2_mag))
    print(v1, v2)
    print(degrees(dtheta))
    
    return dtheta

def getParalletLines(pts, distance):
    leftline = []
    rightline = []
    
    x0, y0 = pts[0]
    x1, y1 = pts[1]
    vector = (x1-x0, y1-y0)
    orientation1 = getAngle((1, 0), vector)

    leftturn = orientation1 + pi / 2
    righrturn = orientation1 - pi / 2
    leftPt = (x0 + distance*cos(leftturn), y0 + distance*sin(leftturn))
    leftline.append(leftPt)
    rightPt = (x0 + distance*cos(righrturn), y0 + distance*sin(righrturn))
    rightline.append(rightPt)
    
    for n in range(1, len(pts)-1):
        print('hello')
        x0, y0 = pts[n-1]
        x1, y1 = pts[n]
        x2, y2 = pts[n+1]
        
        v1 = (x1-x0, y1-y0)
        v2 = (x2-x1, y2-y1)
        dtheta = getAngle(v1, v2)          
        orientation1 = getAngle((1, 0), v1)
        print(degrees(dtheta))
        
        leftturn = orientation1 + dtheta / 2 + pi / 2
        righrturn = orientation1 + dtheta / 2 - pi / 2 
    
        distance2 = distance/sin((pi-dtheta)/2)
        leftPt = (x1 + distance2*cos(leftturn), y1 + distance2*sin(leftturn))
        leftline.append(leftPt)
        rightPt = (x1 + distance2*cos(righrturn), y1 + distance2*sin(righrturn))
        rightline.append(rightPt)
        
    x0, y0 = pts[-2]
    x1, y1 = pts[-1]
    
    vector = (x1-x0, y1-y0)
    orientation1 = getAngle((1, 0), vector)
    leftturn = orientation1 + pi / 2
    righrturn = orientation1 - pi / 2
    leftPt = (x1 + distance*cos(leftturn), y1 + distance*sin(leftturn))
    leftline.append(leftPt)
    rightPt = (x1 + distance*cos(righrturn), y1 + distance*sin(righrturn))
    rightline.append(rightPt)
    return leftline, rightline    
    
def getLocations(line, gap):
    location=[line[0]]
    residual = 0
    
    for n in range(len(line)-1):
        x0, y0 = line[n]
        x1, y1 = line[n+1]
        length = sqrt((x1-x0)**2 + (y1-y0)**2)
        dx, dy = (x1-x0)/length, (y1-y0)/length
        x = x0 - dx * residual
        y = y0 - dy * residual
        length = length + residual
        while length >= gap:
            x += gap*dx
            y += gap*dy
            location.append((x, y))
            length -= gap
          
        residual = length
    return location

via_name = oEditor.GetSelections()[0]
line_name = oEditor.GetSelections()[1]

pts = [i for i in oEditor.GetProperties('BaseElementTab', line_name) if i.startswith('Pt')]
AddWarningMessage(str(pts))

line = []
for i in pts:
    location = oEditor.GetPropertyValue('BaseElementTab', line_name, i)
    x, y = [float(i) for i in location.split(',')]
    line.append((x, y))

AddWarningMessage(str(line))

leftline, rightline = getParalletLines(line, distance)
for x, y in getLocations(rightline, gap) + getLocations(leftline, gap) :
    duplicateNewVia(via_name, x, y)

AddWarningMessage('Run Time:{} sec'.format(time.time()-t0))
