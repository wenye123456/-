
from os import remove
from numpy import delete
import pygame
import math
from func import Get_Angle, Get_Distance
from pyrsistent import v

FPS=30
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
class ShootBulltin(GameObject):
  def __init__(self,pos,direction) -> None:
    super().__init__()
    self.image=pygame.image.load("src\shootbullet1.png")
    self.direction=direction
    if self.direction==1 or self.direction==3:
       self.image=pygame.transform.rotate(self.image,90)
    self.speed=10
    self.rect=self.image.get_rect()
    left,top=pos
    self.rect.left=left
    self.rect.top=top
    self.x:float=self.rect.left
    self.y:float=self.rect.top
    self.life=True
    self.mytype='ShootBulltin'
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
  def update(self):
    if self.direction==0:
      self.y-=self.speed
    if self.direction==1:
      self.x-=self.speed
    if self.direction==2:
      self.y+=self.speed
    if self.direction==3:
      self.x+=self.speed

    self.rect.left=self.x
    self.rect.top=self.y
    if self.Expired():
      self.life=False
    
class Obstacle(GameObject):
  def __init__(self,pos,radius=5,v=(0,0)) -> None:
    super().__init__()
    #self.image=pygame.image.load(r"src\bulltin01_r.png")
    self.image=pygame.image.load(r"src\bomb_supply.png")
    self.image=pygame.transform.scale(self.image,(50,80))
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
    if self.Expired():
      self.life=False
    pass
  def Die(self):
    self.func=self.Explode
    
  def Explode(self):
    self.diecount+=0.5
    path=r"src\bulltin0{0}_r.png".format(math.floor(self.diecount))
    self.image=pygame.image.load(path)
  
    if(self.diecount>=4):
      self.life=False
    

  def Expired(self)->bool:
    if self.rect.left+self.rect.width<=0 or self.rect.left>=WINDOW_WIDTH:
      return True
    if self.rect.top+self.rect.height<=0 or self.rect.top>=WINDOW_HEIGHT:
      return True
    return False

    

  def update(self):
    self.func()
  def Get_pos(self):
    return (self.x,self.y)
  def Type(self):
    return self.mytype