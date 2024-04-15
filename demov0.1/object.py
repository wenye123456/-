
from os import remove
import pygame
import math
from func import Get_Angle, Get_Distance

FPS=60
WINDOW_WIDTH=1280
WINDOW_HEIGHT=720

class GameObject(pygame.sprite.Sprite):
  def __init__(self) -> None:
    super().__init__()
  def Type(self):
    pass

class Target(GameObject):
  def __init__(self,left,top) -> None:
    super().__init__()
    self.image=pygame.image.load("src\space.png")
    self.image=pygame.transform.scale(self.image,(50,50))
    self.rect=self.image.get_rect()
    self.rect.left=left
    self.rect.top=top
    self.radius=self.rect.width/2
    self.mytype='Target'
  def Type(self):
    return self.mytype
  
class Bulltin(GameObject):
  def __init__(self,pos,radius=5,v=(0,0)) -> None:
    super().__init__()
    self.image=pygame.image.load(r"src\bulltin01_r.png")
    self.rect=self.image.get_rect()
    left,top=pos
    self.rect.left=left
    self.rect.top=top
    self.x:float=self.rect.left
    self.y:float=self.rect.top
    
    self.radius=radius
    self.v=v
    self.life=True
    self.mytype='Bulltin'
    self.diecount=1
    self.func=self.Move
  
  def Move(self):
    v_h,v_v=self.v
    self.x+=v_h/FPS
    self.y+=v_v/FPS
    self.rect.left=self.x
    self.rect.top=self.y

    pass
  def Die(self):
    self.func=self.Explode
    
  def Explode(self):
    self.diecount+=0.3
    path=r"src\bulltin0{0}_r.png".format(math.floor(self.diecount))
    self.image=pygame.image.load(path)
  
    if(self.diecount>=4):
      self.life=False
    

  def Expired(self)->bool:
    #     if self.pos["x"]<=0 or self.pos["x"]>=WINDOW_WIDTH:
    #   self.v['x']=-BOUNCE_CONST*self.v['x']
    # if self.pos['y']<=0 or self.pos["y"]>=WINDOW_HEIGHT:
    #   self.v['y']=-BOUNCE_CONST*self.v['y']
    if self.rect.left+self.rect.width<=0 or self.rect.left>=WINDOW_WIDTH:
      return True
    if self.rect.top+self.rect.height<=0 or self.rect.top>=WINDOW_HEIGHT:
      return True
    return False
  def CheckClipLine(self,line)->bool:
    if line==None:
      return  False
    return not self.rect.clipline(line.pos1,line.pos2)==tuple()
    
  
  def Ricochet(self,line):
    if self.rect.clipline(line.pos1,line.pos2)==tuple():
      return
    
    vx,vy=self.v
    x1,y1=line.pos1
    x2,y2=line.pos2
    v_t=(vx,vy)
    flag,angel=Get_Angle(line.pos1,line.pos2,v_t)
    if flag==True:
      r=((x2-x1)/line.len,(y2-y1)/line.len)
    else:
      r=((x1-x2)/line.len,(y1-y2)/line.len)
    vh=(r[0]*Get_Distance((0,0),v_t)*math.cos(math.radians(angel)),r[1]*Get_Distance((0,0),v_t)*math.cos(math.radians(angel)))
    
    vv=(v_t[0]-vh[0],v_t[1]-vh[1])
    vv=(-1*vv[0],-1*vv[1])
    v_new=(vv[0]+vh[0],vv[1]+vh[1])
    self.v=v_new
    #self.v=tuple(i*1.2 for i in v_new)
    #self.Move()
  def update(self):
    self.func()
  def Get_pos(self):
    return (self.x,self.y)
  def Type(self):
    return self.mytype