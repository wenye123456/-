import pygame
INIT_SIZE=100
SCREEN_WIDTH=1280
SCREEN_HEIGHT=720
class Basin(pygame.sprite.Sprite):
  def __init__(self):
    self.image=pygame.image.load(R"src\basin.png")
    self.radio=self.image.get_size()[1]/self.image.get_size()[0]
    new_size=(INIT_SIZE,INIT_SIZE*self.radio)
    self.image=pygame.transform.scale(self.image,new_size)
    self.rect=self.image.get_rect()
    self.rect.top=650
    self.v=0 
    self.v_flag=0
    

    pass
  
  def GetImage(self):
    return self.image
  
  def GetRect(self):
    return self.rect
  def Move(self,left):
    left-=self.rect.width//2
    if left<0:
      left=0
    if left>SCREEN_WIDTH-self.rect.width:
      left=SCREEN_WIDTH-self.rect.width
    if self.rect.top+self.rect.height>SCREEN_HEIGHT:
      self.rect.top=SCREEN_HEIGHT-self.rect.height
    
    self.rect.left=left
  def ImprovedMove(self,left):
    left-=self.rect.width//2
    
    self.v_flag+=1
    if self.v_flag==10:
      self.v_flag=0
      if left<self.rect.left:
        self.v-=3
      if left>self.rect.left:
        self.v+=3
      if self.v>0:
        self.v-=1
      if self.v<0:
        self.v+=1
    self.rect.left+=self.v
    if self.rect.left<0:
      self.rect.left=0
      self.v=0
    if self.rect.left>SCREEN_WIDTH-self.rect.width:
      self.rect.left=SCREEN_WIDTH-self.rect.width
      self.v=0
      
      
    
    
  