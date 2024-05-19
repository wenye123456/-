import pygame
import math
#from  object import GameObject
from func import Get_Angle, Get_Distance

FPS=30
WINDOW_WIDTH=1280
WINDOW_HEIGHT=720

class Plane(pygame.sprite.Sprite):
  def __init__(self,x,y,v=(0,-140)) -> None:
    super().__init__()
    self.pos:dict[str,float]={'x':x,'y':y}
    self.v:dict[str,float]={'x':v[0],'y':v[1]}
    
    
    image_1=pygame.image.load(r"src\me1.png")
    image_2=pygame.image.load(r"src\me2.png")
    image_1=pygame.transform.scale(image_1,(50,50))
    image_2=pygame.transform.scale(image_2,(50,50))
    self.images=[]
    for i in range(0,4):
      self.images.append(image_1)
      self.images.append(image_2)
      image_1=pygame.transform.rotate(image_1,90)
      image_2=pygame.transform.rotate(image_2,90)
    self.currentimage=self.images[2]
    self.direction=0
    self.index=0

    self.rect=self.currentimage.get_rect()
    self.rect.top=y-self.rect.height/2
    self.rect.left=x-self.rect.width/2
    
    self.v_store=(0,0)
    #self.Stop()
    
    pass
  
  def Move(self):
    self.pos['x']=self.pos['x']+self.v['x']/FPS
    self.pos['y']=self.pos['y']+self.v['y']/FPS
    
    if self.pos["x"]<0:
      self.pos["x"]=0
    if self.pos["x"]>WINDOW_WIDTH:
      self.pos["x"]=WINDOW_WIDTH
    if self.pos['y']<0 :
      self.pos["y"]=0
    if self.pos["y"]>WINDOW_HEIGHT:
      self.pos["y"]=WINDOW_HEIGHT

    
    self.rect.left=self.pos['x']-self.rect.width/2
    self.rect.top=self.pos['y']-self.rect.height/2
    
    
    self.index=self.index+1
    self.index=self.index%2
    self.currentimage=self.images[2*self.direction+self.index]
    
    pass
      
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

  
  def Stop(self):
    self.v_store=self.GetV()
    self.SetV((0,0))
  
  def Activate(self):
    print(self.v_store)
    self.SetV(self.v_store)
  
  
    
  