import pygame
import math
#from  object import GameObject
from func import Get_Angle, Get_Distance

FPS=60
WINDOW_WIDTH=1280
WINDOW_HEIGHT=720

class Ball(pygame.sprite.Sprite):
  def __init__(self,x,y,v=(10,10),color=(255,0,0),radius=10) -> None:
    super().__init__()
    self.pos:dict[str,float]={'x':x,'y':y}
    self.v:dict[str,float]={'x':v[0],'y':v[1]}
    self.color=color
    self.radius=radius
    self.rect=pygame.Rect(x-radius,y-radius,radius*2,radius*2)
    self.v_store=(0,0)
    #self.Stop()
    
    pass
  def Move(self):
    self.pos['x']=self.pos['x']+self.v['x']/FPS
    self.pos['y']=self.pos['y']+self.v['y']/FPS

    
    self.rect.left=self.pos['x']-self.radius
    self.rect.top=self.pos['y']-self.radius
    pass
  def Bounce(self):
    BOUNCE_CONST=1.0
    FRICTION_CONST=0.0
    if self.pos["x"]<=0 or self.pos["x"]>=WINDOW_WIDTH:
      self.v['x']=-BOUNCE_CONST*self.v['x']
    if self.pos['y']<=0 or self.pos["y"]>=WINDOW_HEIGHT:
      self.v['y']=-BOUNCE_CONST*self.v['y']
      
    # self.v['x']=math.exp(-FRICTION_CONST/FPS)*self.v['x']
    # self.v['y']=math.exp(-FRICTION_CONST/FPS)*self.v['y']
  def GetPos(self):
    return (self.pos['x'],self.pos['y'])
  
  def SetV(self,v):
    vx,vy=v
    self.v['x']=vx
    self.v['y']=vy
  def GetV(self):
    return (self.v['x'],self.v['y'])
    
  def Accelerate(self,acc):
    self.v['x']+=acc[0]
    self.v['y']+=acc[1]
    
  def Ricochet(self,line):
    if line==None:
      return
    x1,y1=line.pos1
    x2,y2=line.pos2
    v_t=(self.v['x'],self.v['y'])
    flag,angel=Get_Angle(line.pos1,line.pos2,v_t)
    if flag==True:
      r=((x2-x1)/line.len,(y2-y1)/line.len)
    else:
      r=((x1-x2)/line.len,(y1-y2)/line.len)
    vh=(r[0]*Get_Distance((0,0),v_t)*math.cos(math.radians(angel)),r[1]*Get_Distance((0,0),v_t)*math.cos(math.radians(angel)))
    vv=(v_t[0]-vh[0],v_t[1]-vh[1])
    vv=(-1*vv[0],-1*vv[1])
    v_new=(vv[0]+vh[0],vv[1]+vh[1])
    self.SetV(v_new)
    
  def CheckLine(self,line)->bool:
    if line==None:
      return
    if self.rect.clipline(line.pos1,line.pos2)!=tuple():
      return True
    return False
  
  # def CheckObject(self,objectitem:GameObject)->int:
  #   if pygame.sprite.collide_circle(self,objectitem):
  #     return objectitem.type
  #   return 0
  
  def Stop(self):
    self.v_store=self.GetV()
    self.SetV((0,0))
  
  def Activate(self):
    print(self.v_store)
    self.SetV(self.v_store)
  
  
    
  