
import pygame
SCREEN_WIDTH=1280
SCREEN_HEIGHT=720
FPS=60

class YuanBao(pygame.sprite.Sprite):
  def __init__(self,left=0,top=0,speed=5):
    self.image=pygame.image.load(R"src\元宝.png")
    self.image=pygame.transform.scale(self.image,(40,20))
    self.rect=self.image.get_rect()
    
    
    if left>SCREEN_WIDTH-self.rect.width:
      left=SCREEN_WIDTH-self.rect.width
    self.rect.top=top
    self.rect.left=left
    
    self.living=True
    self.speed=speed
    pass
  
  def GetImage(self):
    return self.image
  
  def GetRect(self):
    return self.rect
  def Move(self):

    if self.rect.top+self.rect.height>SCREEN_HEIGHT:
      self.rect.top=SCREEN_HEIGHT-self.rect.height
    self.rect.top+=self.speed
    
    if self.rect.top>=SCREEN_HEIGHT-self.rect.height:
      self.living=False
    
