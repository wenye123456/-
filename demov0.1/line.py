from turtle import color
from numpy import angle
import pygame
import math
from func import Get_Distance
import random
class Line():
  
  def __init__(self,pos1,pos2,color=(255,0,0)) -> None:
    self.pos1=pos1
    self.pos2=pos2
    self.len=Get_Distance(self.pos1,self.pos2)
    self.color=color
    self.angle=math.atan2(pos2[1]-pos1[1],pos2[0]-pos1[0])
    self.angle=math.degrees(self.angle)
    pass
  def isvaild(self):
    pass
  def Move(self,pos1,pos2):
    self.pos1=pos1
    self.pos2=pos2
  def Ricochet(self):
    pass
  def RandomColor(self):
    self.color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
  def equal(self,line)->bool:
    return self.pos1==line.pos1 and self.pos2==line.pos2
    
  