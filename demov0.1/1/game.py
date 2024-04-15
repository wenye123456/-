import pygame
import random
import cv2
import time
from basin import Basin
from yuanbao import YuanBao
from music import Music
from HandUtils import HandDetector

FPS=60
CAREMA_COUNT=3
TIME_EVENT=pygame.USEREVENT
#TIME_EVENT=pygame.USEREVENT+1
FPS_Timelist=[]
Hand_Timelist=[]

carema=cv2.VideoCapture(0)
    
class MainGame():
  def __init__(self):
    MainGame.running=False
    MainGame.basin=Basin()
    MainGame.yuanbao_list:list[YuanBao]=[]
    MainGame.point=0
    MainGame.windownumber=0
    MainGame.downrate=1000
    MainGame.musicplayer=Music()
    MainGame.backgroundimg=pygame.image.load(R"src\wall-21534_1920.jpg")
    MainGame.mouseimg=pygame.image.load(R"src\mouse.png")
    MainGame.mousePos=None
    MainGame.count=0
    MainGame.handdetector=HandDetector()
    
    pass
  
  def StartGame(self):
    pygame.init()
    self.TextInit()
    hand_time=0
    MainGame.window = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("demo")
    clock = pygame.time.Clock()
    MainGame.running = True
    pygame.time.set_timer(TIME_EVENT,1000)
    MainGame.musicplayer.PlayBackgroundMusic()
    while MainGame.running:
      start_time=time.time()
      MainGame.count+=1
      if MainGame.count==CAREMA_COUNT:
        MainGame.count=0
        flag,img=carema.read()
        #print("识别")
        if flag:
          Hand_Timelist.append(time.time()-hand_time)
          hand_time=time.time()
          img=cv2.resize(img,(800,600))
          img=cv2.flip(img,1)
          MainGame.handdetector.process(img)
          position=MainGame.handdetector.find_position(img)
          left_finger=position['Right'].get(8,None)
          if left_finger:
            MainGame.mousePos=(left_finger[0]/800*1280,left_finger[1]/600*720)
            self.basin.Move(left_finger[0]/800*1280)
          img=cv2.resize(img,(400,300))
          cv2.imshow("1",img)
          cv2.waitKey(1)
          pass
        else:
          print("读取失败")
      MainGame.window.fill(pygame.Color(0,0,0))
      self.EventHandle()
      if MainGame.windownumber==0:
        MainGame.window.blit(self.backgroundimg,self.backgroundimg.get_rect())
        self.ShowElement()
        self.UpdateElement()
        #self.basin.Move(pygame.mouse.get_pos()[0])
        #self.basin.ImprovedMove(pygame.mouse.get_pos()[0])
      if MainGame.windownumber==1:
        self.DrawData()
      
      pygame.display.update()
      clock.tick(FPS)
      end_time=time.time()
      FPS_Timelist.append(end_time-start_time)

    pass
  def EndGame(self):
    MainGame.running=False
    global FPS_Timelist
    global Hand_Timelist
    FPS_Timelist=FPS_Timelist[-100:]
    Hand_Timelist=Hand_Timelist[-100:]
    print("帧间隔：{0}s,手势识别帧间隔：{1}s".format(
      sum(FPS_Timelist)/len(FPS_Timelist),
      sum(Hand_Timelist)/len(Hand_Timelist)
    ))
    
    
  
  def EventHandle(self):
    eventlist=pygame.event.get()
    for event in eventlist:
      if event.type==pygame.QUIT:
        self.EndGame()
      if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_p:
          MainGame.windownumber=1
          pass
        if event.key==pygame.K_0:
          print(len(MainGame.yuanbao_list))
          pass
        if event.key==pygame.K_1:
          pygame.time.set_timer(TIME_EVENT,500)
          pass
        if event.key==pygame.K_SPACE:
          pass
      if event.type==pygame.KEYUP:
        if event.key==pygame.K_p:
          MainGame.windownumber=0
          pass
      if event.type==TIME_EVENT:
        MainGame.downrate=random.randint(500,2000)
        pygame.time.set_timer(TIME_EVENT,MainGame.downrate)
        if MainGame.windownumber==0:
          self.CreateYuanBao()


  def ShowElement(self):
    MainGame.window .blit(self.basin.GetImage(),self.basin.GetRect())
    for yuanbao in MainGame.yuanbao_list:
        MainGame.window.blit(yuanbao.GetImage(),yuanbao.GetRect())
    if MainGame.mousePos !=None:
      rect=MainGame.mouseimg.get_rect()
      rect.left=MainGame.mousePos[0]
      rect.top=MainGame.mousePos[1]
      MainGame.window.blit(MainGame.mouseimg,rect)
  def UpdateElement(self):
    for yuanbao in MainGame.yuanbao_list:
        yuanbao.Move()
        if pygame.sprite.collide_rect(MainGame.basin,yuanbao):
          MainGame.musicplayer.PlaySound()
          MainGame.point+=1
          yuanbao.living=False
          print("碰撞")
        if yuanbao.living==False:
          MainGame.yuanbao_list.remove(yuanbao)
        
    pass
  def CreateYuanBao(self):
    # if random.randint(0,1000)<30:
    MainGame.yuanbao_list.append(YuanBao(left=random.randint(0,1280)))
    pass
  def TextInit(self):
    pygame.font.init()
    self.font=pygame.font.SysFont('dengxian',18)
  def DrawData(self):
    MainGame.window.blit(self.font.render("point:{0}".format(MainGame.point),True,pygame.Color(255,255,255)),(20,20))
    #MainGame.window.blit(self.GetTextSurface("heath:{0}".format(MainGame.my_tank.heath)),(0,20))
 

if __name__=='__main__':
  MainGame().StartGame()
  carema.release()
  print("退出")