
from turtle import width
import pygame
import cv2
import time
import math
from line import Line
from HandUtils import HandDetector
from HandUtils import BlendImage
from func import Get_Angle, Get_Distance
from  object import GameObject
from  object import Bulltin
import random
import copy
from ball import Ball
from music import MusicPlayer


FPS=30
CAREMA_COUNT=3
WINDOW_WIDTH=1280
WINDOW_HEIGHT=720
DEBUG=0
CLICK_EVENT=pygame.USEREVENT
TIMER1_EVENT=pygame.USEREVENT+1
FAIL_EVENT=pygame.USEREVENT+2
carema=cv2.VideoCapture(1)
hand_detector=HandDetector()






class MainGame():
  def __init__(self):
    MainGame.window=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    MainGame.balllist:list[Ball]=[]
    MainGame.objectlist:list[GameObject]=[]
    MainGame.ball:Ball=None
    #MainGame.linelist:list[Line]=[]
    
    MainGame.count=0
    MainGame.line:Line=None
    MainGame.thumbpos=None
    MainGame.indexfingerpos=None
    MainGame.thumbimage=pygame.image.load("src\mouse.png")
    MainGame.indexfingerimage=pygame.image.load("src\mouse.png")
    MainGame.ballgroup=pygame.sprite.Group()
    MainGame.objectgroup=pygame.sprite.Group()
    MainGame.time=None
    MainGame.clickcooldown=False
    MainGame.font=None
    MainGame.currentpage=0
    MainGame.starttime=0
    MainGame.background_image=pygame.image.load(r"src\background.png")
    MainGame.musicplayer=MusicPlayer()
    
    
    pass
    
  def render(self):
    MainGame.window.fill(pygame.Color(0,0,0))
    if MainGame.currentpage==0:
      MainGame.window.blit(MainGame.background_image,(0,0))
      if MainGame.ball!=None:
        x=MainGame.ball.pos['x']
        y=MainGame.ball.pos['y']
        pygame.draw.circle(surface=MainGame.window,center=(x,y),radius=MainGame.ball.radius,color=MainGame.ball.color)
      
      MainGame.objectgroup.draw(MainGame.window)
      if MainGame.line!=None:
        pygame.draw.line(surface=MainGame.window,start_pos=MainGame.line.pos1,end_pos=MainGame.line.pos2,
                      color=MainGame.line.color,width=5)


      if self.thumbpos!=None:
        MainGame.window.blit(self.thumbimage,dest=self.thumbpos)
      if self.indexfingerpos!=None:
        MainGame.window.blit(self.thumbimage,dest=self.indexfingerpos)
      MainGame.window.blit(MainGame.font.render(MainGame.time,True, (255, 255, 255)),(0,0))
    if MainGame.currentpage==1:
      font=pygame.font.SysFont('SimHei ',100)
      MainGame.window.blit(font.render("你的成绩为",True, (255, 255, 255)),(400,200))
      MainGame.window.blit(font.render(MainGame.time,True, (255, 255, 255)),(600,300))
      
      
    pygame.display.update()
  def event_handle(self):
    eventlist=pygame.event.get()
    for event in eventlist:
      if event.type==pygame.QUIT:
        exit()
      if event.type==pygame.KEYUP:
        if MainGame.currentpage==1:
          if event.key==pygame.K_r:
            MainGame.starttime=pygame.time.get_ticks()
            MainGame.currentpage=0
            MainGame.objectgroup.empty()
            MainGame.ball=Ball(WINDOW_WIDTH/2,WINDOW_HEIGHT/2,v=(0,280),color=(255,0,255))
      if event.type==CLICK_EVENT:
        if MainGame.clickcooldown==False:
          print("click")
          
          MainGame.clickcooldown=True
          pygame.time.set_timer(TIMER1_EVENT,1000)
          MainGame.musicplayer.PlaySound()
          if MainGame.ball!=None:
            if MainGame.ball.GetV()==(0,0):
              MainGame.ball.Activate()
            else:
              MainGame.ball.Stop()
              
      if event.type==TIMER1_EVENT:
        MainGame.clickcooldown=False
      if event.type==FAIL_EVENT:
        if DEBUG:
          return
        MainGame.currentpage=1#fail page
        #print(1)
        pass
           

  def update(self):
    if MainGame.currentpage!=0:
      return

    if MainGame.ball.CheckLine(MainGame.line):
      MainGame.ball.Ricochet(MainGame.line)
    MainGame.ball.Bounce()
    MainGame.ball.Move()
    MainGame.objectgroup.update()
    for spire in MainGame.objectgroup.sprites():
      if spire.life==False:
        MainGame.objectgroup.remove(spire)
        continue
      if spire.Expired():
        MainGame.objectgroup.remove(spire)
        continue
      if spire.CheckClipLine(MainGame.line):
        spire.Die()
      #spire.Ricochet(MainGame.line)
      
    self.CreateBulltin()
    
    

    t=pygame.sprite.spritecollide(MainGame.ball,MainGame.objectgroup,False)
    if len(t)>0:
      MainGame.musicplayer.PlayExplode()
      MainGame.ball=None
      pass
    #time
    second=(int)((pygame.time.get_ticks()-MainGame.starttime)/1000)
    min,sec=divmod(second,60)
    MainGame.time="{0}:{1}".format(min,sec)
    if MainGame.ball==None:
      pygame.event.post(pygame.event.Event(FAIL_EVENT)) 
    pass
  
  
  def run(self):
   
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    #MainGame.line=Line((50,450),(650,650))
    
    MainGame.ball=Ball(WINDOW_WIDTH/2,WINDOW_HEIGHT/2,v=(0,280),color=(255,0,255))
    
    
    MainGame.font=pygame.font.SysFont('SimHei ',18)
    
    

    while True:
      MainGame.count=MainGame.count+1
      if MainGame.count==CAREMA_COUNT:
        MainGame.count=0
        
        flag,img=carema.read()
        
        if flag and MainGame.currentpage==0:
          img=cv2.resize(img,(800,600))
          img=cv2.flip(img,1)
          hand_detector.process(img)
          position=hand_detector.find_position(img)
          
          pos1=position['Right'].get(4,None)
          pos2=position['Right'].get(8,None)
          
          if pos1!=None and pos2!=None:
            MainGame.thumbpos=(WINDOW_WIDTH*float(pos1[0])/800,WINDOW_HEIGHT*float(pos1[1])/600)
            MainGame.indexfingerpos=(WINDOW_WIDTH*float(pos2[0])/800,WINDOW_HEIGHT*float(pos2[1])/600)

          if hand_detector.click():
            pygame.event.post(pygame.event.Event(CLICK_EVENT)) 
            pass
          if hand_detector.isleft():
              if MainGame.ball.pos['x']>20:

                x,y=MainGame.ball.GetV()
                t=math.hypot(x,y)
                MainGame.ball.SetV((t,0))
              print("left_event")
              pass
          elif hand_detector.isright():
            if WINDOW_WIDTH-MainGame.ball.pos['x']>20:

              x,y=MainGame.ball.GetV()
              t=-1*math.hypot(x,y)
              MainGame.ball.SetV((t,0))
            print("right_event")
          elif hand_detector.isup():
            if MainGame.ball.pos['y']>20:
              x,y=MainGame.ball.GetV()
              t=-1*math.hypot(x,y)
              MainGame.ball.SetV((0,t))
            print("up_event")
            pass
          elif hand_detector.isdown():
            if WINDOW_HEIGHT-MainGame.ball.pos['y']>20:
              x,y=MainGame.ball.GetV()
              t=math.hypot(x,y)
              MainGame.ball.SetV((0,t))
                
            print("down_event")
            pass
            
          cv2.imshow("1",img)
          cv2.waitKey(1)
      
      self.update()
      self.render()
      self.event_handle()
      clock.tick(FPS)
  def Attract(self):
    G:float= 1e6/FPS
    # for ball1 in self.balllist:
    #   for ball2 in self.balllist:
    #     if ball1==ball2:
    #       continue
    #     pos1=ball1.GetPos()
    #     pos2=ball2.GetPos()
    #     rlen=self.Get_Distance(pos1,pos2)
    #     if rlen<10:
    #       continue
    #     force=G/(rlen*rlen)
    #     acc=(force/rlen*(pos2[0]-pos1[0]),force/rlen*(pos2[1]-pos1[1]))
    #     ball1.Accelerate(acc)
        
  def Get_Distance(self,p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    length = math.hypot(x2 - x1, y2 - y1)
    return length
    pass
  
  def CreateLine(self,start_pos,end_pos):
    
    line_t=Line(start_pos,end_pos,MainGame.line.color)
    # if abs(line_t.angle-MainGame.line.angle)<10:
    #   return 
    if abs(line_t.angle-MainGame.line.angle)<10 and abs(line_t.len-MainGame.line.len)<20:
      return 
    if abs(line_t.len-MainGame.line.len)<20:
      return 

    if line_t.len>50:
      MainGame.line=line_t
  def CreateBulltin(self):
    Bulltin_number=3+0.1*(pygame.time.get_ticks()-MainGame.starttime)/1000
    if len(MainGame.objectgroup)>=math.floor(Bulltin_number):
      return
    pos=random.randint(0,WINDOW_WIDTH),random.randint(0,WINDOW_HEIGHT)
    pos=list(pos)
    v_t=random.randint(40,180),random.randint(40,180)
    v_t=list(v_t)
    if random.randint(0,1):
      v_t[0]=-v_t[0]
    if random.randint(0,1):
      v_t[1]=-v_t[1]
      
    
    flag=random.randint(0,3)
    if flag==0:
      pos[0]=0-50
    if flag==1:
      pos[0]=WINDOW_WIDTH
    if flag==2:
      pos[1]=0-50
    if flag==3:
      pos[1]=WINDOW_HEIGHT
    MainGame.objectgroup.add(Bulltin(pos=pos,v=v_t))
    #MainGame.objectgroup.add(Bulltin(pos=(300,300),v=v_t))
    
    pass
MainGame().run()
  