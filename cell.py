# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 14:39:10 2023

@author: 42496
"""

class cell():
  def __init__(self,row,col,maxRow,maxCol):
    self.row = row
    self.col = col
    self.loc = [row,col]
    self.program = 0
    self.access = 0
    self.accessOut = 0
    self.maxRow = maxRow
    self.maxCol = maxCol
    self.corner = 0
    self.lstNeighbor = []
    self.detectBound()
    self.detectNeighbor()
    self.detectCorner()

  def assign(self,program,mapCore):
    self.program = program
    mapCore[self.row,self.col] = program
  
  def refresh(self):
    self.program = 0

  def detectBound(self):
    if self.row == 0 or self.row == self.maxRow -1 or self.col == 0 or self.col == self.maxCol - 1:
      self.access = 1
      self.accessOut = 1
    return self.access, self.accessOut
  
  def detectCorner(self):
    if self.row == 0 or self.row == self.maxRow - 1:
      if self.col == 0 or self.col == self.maxCol - 1:
        self.corner = 1
    return self.corner

  def detectAccess(self,lstCell):
    for i,coordinates in enumerate(self.lstNeighbor):
      iRow = coordinates[0]
      iCol = coordinates[1]
      cellNeighbor = lstCell[iRow][iCol]
      if cellNeighbor.program in (1,3,5):
        self.access = 1
        return self.access

  def detectNeighbor(self):
    self.lstRawNeighbor = [[self.row + 1, self.col],[self.row, self.col + 1],
                           [self.row - 1, self.col],[self.row, self.col - 1]]
    self.lstNeighbor = [coordinates for coordinates in self.lstRawNeighbor if 
                        (coordinates[0] in range(0,self.maxRow) and coordinates[1] in range(0,self.maxCol))]
    return self.lstNeighbor