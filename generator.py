# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 14:22:49 2023

@author: 42496
"""

#Layout Generating Functions
from cell import cell
import numpy as np
import math
import matplotlib.pyplot as plt
import random as rnd
import seaborn as sns
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import time
from scipy.spatial.distance import cdist
import openpyxl
from openpyxl import Workbook
import traceback


def findProgram(lstCell,strProgram):
    lstTarget = []
    iProgram = programDict[strProgram]
    for row in lstCell:
        for stuff in row:
            if stuff.program == iProgram:
                lstTarget.append(stuff.loc)
    return lstTarget

def findAccess(lstCell):
  lstAccess = [] 
  for row in lstCell:
    for stuff in row:
      stuff.detectAccess(lstCell)
      if stuff.access == 1 and stuff.program == 0:
        lstAccess.append(stuff.loc)
  return lstAccess

def createElevatorLobby (lstCell,mapCore,lstBase,elevLobbyAmount,strProgram,other):
    #lstBase here is a placeholder that doesn't get called
    straight = other
    iProgram = programDict[strProgram]
    cElevLobby = []
    lstAvailableStart = []
    for i,row in enumerate(lstCell):
      for j,block in enumerate(row):
        if block.accessOut == 1 and block.corner == 0 and block.program == 0:
          lstAvailableStart.append([i,j])
    iStart = rnd.randint(0,len(lstAvailableStart)-1)
    iRow = lstAvailableStart[iStart][0]
    iCol = lstAvailableStart[iStart][1]
    elevLobbyStart = lstCell[iRow][iCol]
    elevLobbyStart.assign(iProgram,mapCore)
    cElevLobby.append([iRow,iCol])
  
    if straight == 1:
      if elevLobbyStart.row == 0:
        coX,coY = 1,0
      elif elevLobbyStart.row == elevLobbyStart.maxRow-1:
        coX,coY = -1,0
      elif elevLobbyStart.col == 0:
        coX,coY = 0,1
      elif elevLobbyStart.col == elevLobbyStart.maxCol-1:
        coX,coY = 0,-1
        
      cellLast = elevLobbyStart
      for i in range(elevLobbyAmount-1):
        if lstCell[cellLast.row + 1*coX][cellLast.col + 1*coY].program == 0:
          cellNext = lstCell[cellLast.row + 1*coX][cellLast.col + 1*coY]
          cellNext.assign(iProgram, mapCore)
          cElevLobby.append([cellLast.row + 1*coX,cellLast.col + 1*coY])
          cellLast = cellNext
          
          madeIt = True
        else:
            madeIt = False
            if not muted:
                print ('Not Enough room for ' + strProgram)
            break
  
    else:
        madeIt = True
        cellLast = elevLobbyStart
        for i in range(elevLobbyAmount-1):
          lstRawNeighbor = cellLast.lstNeighbor
          lstNeighbor = [iNeighbor for iNeighbor in lstRawNeighbor 
                        if lstCell[iNeighbor[0]][iNeighbor[1]].program == 0]
          if len(lstNeighbor) > 0:
            iNext = rnd.randint(0,len(lstNeighbor)-1)
            cNext = lstNeighbor[iNext]
            cellNext = lstCell[cNext[0]][cNext[1]]
            cellNext.assign(iProgram,mapCore)
            cElevLobby.append(cNext)
            cellLast = cellNext
          else:
              madeIt = False
              if not muted:
                  print ('Not Enough room for ' + strProgram)
              break
    return madeIt

def createGuestElevByClosest(lstCell,mapCore,baseProgram,elevAmount,strProgram,other):
    iProgram = programDict[strProgram]
    cList = []
    lstRawElev = []
    cElevLobby = findProgram(lstCell,baseProgram)
    
    for coordinate in cElevLobby:
      stuff = lstCell[coordinate[0]][coordinate[1]].lstNeighbor
      lstRawElev.extend(stuff)
    lstElev = [list(i) for i in set(map(tuple, lstRawElev))]
    cAvail = [c for c in lstElev if c not in cElevLobby]
    cAvail = [c for c in cAvail if lstCell[c[0]][c[1]].program == 0]
    if len(cAvail) >= elevAmount:
        cBase = rnd.choice(cElevLobby)
        aBase = np.asarray(cBase).reshape(1,2)
        aAvail = np.asarray(cAvail)
        aDis = cdist(aBase,aAvail)
        aOrder = np.argsort(aDis)
        cAvail = aAvail[aOrder].tolist()[0]
        for i in range(elevAmount):
            coordinates = cAvail[i]
            iRow = coordinates[0]
            iCol = coordinates[1]
            lstCell[iRow][iCol].assign(iProgram,mapCore)
            cList.append(coordinates)
        madeIt = True
              
    else:
        madeIt = False
        if not muted:
            print ('Not Enough room for ' + strProgram)
    return madeIt


def createFromAccessible(lstCell,mapCore,baseProgram,amount,strProgram,other):
    #THIS WHOLE FUNCTION SHOULD BE REPLACED BY A DFS RECURSION IN THE FUTURE
    cList = []
    iProgram = programDict[strProgram]
    if baseProgram:
        lstTarget = findProgram(lstCell,baseProgram)  
        lstAccess = []
        for coordinates in lstTarget:
            iRow = coordinates[0]
            iCol = coordinates[1]
            for cN in lstCell[iRow][iCol].lstNeighbor:
                if lstCell[cN[0]][cN[1]].program == 0 and cN not in lstAccess:
                    lstAccess.append(cN)
    else:
        lstAccess = findAccess(lstCell)
    
    if len(lstAccess) > 0:
        rnd.shuffle(lstAccess)
        
        if amount == 2:
            for i, coordinates in enumerate(lstAccess):
                iRow = coordinates[0]
                iCol = coordinates[1]
                lstN = lstCell[iRow][iCol].lstNeighbor
                lstAvl = [c for c in lstN if lstCell[c[0]][c[1]].program == 0]
                if len(lstAvl) > 0:
                  lstCell[iRow][iCol].assign(iProgram,mapCore)
                  cList.append(coordinates)
                  rnd.shuffle(lstAvl)
                  iRow_b = lstAvl[0][0]
                  iCol_b = lstAvl[0][1]
                  lstCell[iRow_b][iCol_b].assign(iProgram,mapCore)
                  cList.append(lstAvl[0])
                  break
        
        else:
            for i in range(amount):
                if len(lstAccess) == 0:
                    break
                
                coordinates = rnd.choice(lstAccess)
                iRow = coordinates[0]
                iCol = coordinates[1]
                lstCell[iRow][iCol].assign(iProgram,mapCore)
                cList.append(coordinates)
                lstN = lstCell[iRow][iCol].lstNeighbor
                lstAccess = [c for c in lstN if lstCell[c[0]][c[1]].program == 0]         
        
    if len(cList) < amount:
        if not muted:
            print ('Not Enough room for ' + strProgram)
        madeIt = False
    else:
        madeIt = True
    
    return madeIt


#Global Initiate
muted = True
efficient = True
dictProgram = {0:'N/A', 1:'L_1', 2:'GE_1', 3 :'L_2', 4:'GE_2',5:'L_3',6:'GE_3',7:'L_4',8:'GE_4',
                 9:'V_1', 10:'FE', 11:'S_1', 12:'V_2', 13:'S_2', 14:'ADA', 15:'MEP', 16:'SHAFT', 17:'AC'}
programDict = {value: key for key, value in dictProgram.items()}


def generate(maxRow, maxCol,lstFuncs):
    lstCell = [[cell(i,j,maxRow,maxCol) for j in range(maxCol)] for i in range(maxRow)]
    mapCore = np.zeros((maxRow,maxCol)) 
    
    for stuff in lstFuncs:
        func = stuff[0]
        madeIt = func(lstCell, mapCore, stuff[1],stuff[2],stuff[3],stuff[4])
       
        if efficient and not madeIt:
            break
    
    
    return lstCell,mapCore,dictProgram,programDict


