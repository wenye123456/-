
import pygame
import cv2
import time
import math
from HandUtils import HandDetector
from HandUtils import BlendImage
from func import Get_Angle, Get_Distance
from  object import GameObject, ShootBulltin
from  object import Obstacle
import random
import copy
from music import MusicPlayer
from plane import Plane



FPS=30
CAREMA_COUNT=3
WINDOW_WIDTH=1280
WINDOW_HEIGHT=720
#游戏参数设置
# DEBUG=1
# fps_time=0.0
# hand_time=0.0
# handtime_list=[]
# fpstime_list=[]


#自定义事件
CLICK_EVENT=pygame.USEREVENT
TIMER1_EVENT=pygame.USEREVENT+1
FAIL_EVENT=pygame.USEREVENT+2
SHOOT_EVENT=pygame.USEREVENT+3
TIMER2_EVENT=pygame.USEREVENT+4

#初始化摄像头与手势识别类
# carema=cv2.VideoCapture(0)
# hand_detector=HandDetector()

carema=None
hand_detector=None






class MainGame():
  #初始化
  def __init__(self):
    
    MainGame.window=pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    MainGame.plane:Plane=None
    MainGame.count=0
    MainGame.indexfingerpos_r=None
    MainGame.indexfingerpos_l=None
    MainGame.indexfingerimage_r=pygame.image.load("src\mouse.png")
    MainGame.indexfingerimage_l=pygame.image.load("src\mouse.png")
    
    MainGame.objectgroup=pygame.sprite.Group()
    MainGame.shootgroup=pygame.sprite.Group()
    MainGame.time=None
    
    MainGame.clickcooldown=False
    MainGame.shootcooldown=False
    MainGame.font=None
    MainGame.currentpage=0
    MainGame.starttime=0
    MainGame.background_image_total=pygame.image.load(r"src\background.png")
    MainGame.background_pos=0         #1866:背景图长度
    MainGame.musicplayer=MusicPlayer()
    
    MainGame.carema=None
    MainGame.hand_detector=None

    
    
    pass
    # 图形渲染函数
  def render(self):
    MainGame.window.fill(pygame.Color(0,0,0))
    if MainGame.currentpage==0:
      MainGame.window.blit(MainGame.background_image,(0,0))
        
      if MainGame.plane!=None:
        MainGame.window.blit(MainGame.plane.currentimage,MainGame.plane.rect)
        
        
      MainGame.objectgroup.draw(MainGame.window)
      MainGame.shootgroup.draw(MainGame.window)



      if self.indexfingerpos_r!=None:
        MainGame.window.blit(self.indexfingerimage_r,dest=self.indexfingerpos_r)
      if self.indexfingerpos_l!=None:
        MainGame.window.blit(self.indexfingerimage_l,dest=self.indexfingerpos_l)
      MainGame.window.blit(MainGame.font.render(MainGame.time,True, (255, 255, 255)),(0,0))
    if MainGame.currentpage==1:
      font=pygame.font.SysFont('SimHei ',100)
      MainGame.window.blit(font.render("你的成绩为",True, (255, 255, 255)),(400,200))
      MainGame.window.blit(font.render(MainGame.time,True, (255, 255, 255)),(600,300))
      
      
    pygame.display.update()
    #事件处理函数
  def event_handle(self):
    eventlist=pygame.event.get()
    for event in eventlist:
      if event.type==pygame.QUIT:
        # global fpstime_list
        # global handtime_list
        # print("手势识别间隔：{0}  fps间隔:{1}".format(sum(handtime_list)/100,sum(fpstime_list)/100))
        exit()
      if event.type==pygame.KEYUP:
        if MainGame.currentpage==1:
          if event.key==pygame.K_r:
            MainGame.starttime=pygame.time.get_ticks()
            MainGame.currentpage=0
            MainGame.objectgroup.empty()
            MainGame.plane=Plane(WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
      if event.type==CLICK_EVENT:
        if MainGame.clickcooldown==False:
          print("click")
          
          MainGame.clickcooldown=True
          pygame.time.set_timer(TIMER1_EVENT,1500)
          MainGame.musicplayer.PlaySound()
          if MainGame.plane!=None:
            if MainGame.plane.GetV()==(0,0):
              MainGame.plane.Activate()
            else:
              MainGame.plane.Stop()
      if event.type==SHOOT_EVENT:
        if MainGame.shootcooldown==False:
          
          MainGame.shootcooldown=True
          pygame.time.set_timer(TIMER2_EVENT,1000)
          self.CreateShoot()
          
      if event.type==TIMER1_EVENT:
        MainGame.clickcooldown=False
      if event.type==TIMER2_EVENT:
        MainGame.shootcooldown=False
      if event.type==FAIL_EVENT:
        MainGame.currentpage=1#fail page
        pass
           

  def update(self):
    # 游戏界面控制
    if MainGame.currentpage!=0:
      return


    MainGame.plane.Move()
    MainGame.objectgroup.update()
    MainGame.shootgroup.update()
    
    
    #检查游戏对象寿命
    for spire in MainGame.objectgroup.sprites():
      if spire.life==False:
        MainGame.objectgroup.remove(spire)
    for spire in MainGame.shootgroup.sprites():
      if spire.life==False:
        MainGame.shootgroup.remove(spire)

      
    self.CreateObstacle()

#碰撞检测
    objectlist=pygame.sprite.groupcollide(MainGame.objectgroup,MainGame.shootgroup,dokilla=False,dokillb=True)
    if len(objectlist)!=0:
      for object in objectlist:
        MainGame.musicplayer.PlayExplode()
        object.Die()
    t=pygame.sprite.spritecollide(MainGame.plane,MainGame.objectgroup,False)
    if len(t)>0:
      MainGame.musicplayer.PlayExplode()
      MainGame.plane=None
    
    #背景移动
    MainGame.background_pos=MainGame.background_pos+5
    MainGame.background_pos=MainGame.background_pos%1866
    MainGame.background_image=MainGame.background_image_total.subsurface((0,MainGame.background_pos,1280,720))
    
    #time显示
    second=(int)((pygame.time.get_ticks()-MainGame.starttime)/1000)
    min,sec=divmod(second,60)
    MainGame.time="{0}:{1}".format(min,sec)
    
    #失败判断
    if MainGame.plane==None:
      print(1)
      pygame.event.post(pygame.event.Event(FAIL_EVENT)) 
    pass
  
  
  def run(self):
    #初始化
    MainGame.carema=cv2.VideoCapture(0)
    MainGame.hand_detector=HandDetector()
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    MainGame.plane=Plane(WINDOW_WIDTH/2,WINDOW_HEIGHT/2)
    MainGame.font=pygame.font.SysFont('SimHei ',18)
    MainGame.musicplayer.PlayBackgroundMusic()

    while True:
      self.Detector_Hand()  #手势识别
      self.update()         #更新游戏元素
      self.render()         #绘制游戏元素
      self.event_handle()   #事件处理
      clock.tick(FPS)       #帧率控制
      # if DEBUG:
      #   global fpstime_list
      #   global fps_time
      #   fpstime_list.append(time.time()-fps_time)
      #   if len(fpstime_list)>100:
      #     fpstime_list=fpstime_list[-100:]
      #   fps_time=time.time()
      
  
  def Detector_Hand(self):
    MainGame.count=MainGame.count+1
    if MainGame.count==CAREMA_COUNT:
      MainGame.count=0
      
      flag,img=MainGame.carema.read()
      
      if flag and MainGame.currentpage==0:
        img=cv2.resize(img,(800,600))
        img=cv2.flip(img,1)
        MainGame.hand_detector.process(img)
        position=MainGame.hand_detector.find_position(img)
        
        # 在更新鼠标位置
        pos1=position['Left'].get(8,None)
        pos2=position['Right'].get(8,None)
        if pos1!=None:
          MainGame.indexfingerpos_r=(WINDOW_WIDTH*float(pos1[0])/800,WINDOW_HEIGHT*float(pos1[1])/600)
        else:
          MainGame.indexfingerpos_r=None
        if pos2!=None:
          MainGame.indexfingerpos_l=(WINDOW_WIDTH*float(pos2[0])/800,WINDOW_HEIGHT*float(pos2[1])/600)
        else:
          MainGame.indexfingerpos_l=None
        
        if MainGame.hand_detector.isclick():
          pygame.event.post(pygame.event.Event(CLICK_EVENT)) 
          pass
        if MainGame.hand_detector.isshoot():
          pygame.event.post(pygame.event.Event(SHOOT_EVENT)) 
          pass
        if MainGame.hand_detector.isleft():
            x,y=MainGame.plane.GetV() 
            t=math.hypot(x,y)
            MainGame.plane.SetV((t,0))
            if t!=0:
              MainGame.plane.direction=3
              print("left_event")
            pass
        elif MainGame.hand_detector.isright():
          x,y=MainGame.plane.GetV()
          t=-1*math.hypot(x,y)
          if t!=0:
            MainGame.plane.SetV((t,0))
            MainGame.plane.direction=1
          print("right_event")
        elif MainGame.hand_detector.isup():
          if MainGame.plane.pos['y']>20:
            x,y=MainGame.plane.GetV()
            t=-1*math.hypot(x,y)
            if t!=0:
              MainGame.plane.SetV((0,t))
              MainGame.plane.direction=0
          print("up_event")
          pass
        elif MainGame.hand_detector.isdown():
          if WINDOW_HEIGHT-MainGame.plane.pos['y']>20:
            x,y=MainGame.plane.GetV()
            t=math.hypot(x,y)
            if t!=0:
              MainGame.plane.SetV((0,t))
              MainGame.plane.direction=2
          print("down_event")
          pass
        img=cv2.resize(img,(400,300))
        cv2.imshow("1",img)
        cv2.waitKey(1)
        
        # if DEBUG:   测试代码
        #   global hand_time
        #   global handtime_list
        #   handtime_list.append(time.time()-hand_time)
        #   if len(handtime_list)>100:
        #     handtime_list=handtime_list[-100:]
        #   hand_time=time.time()

  def Get_Distance(self,p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    length = math.hypot(x2 - x1, y2 - y1)
    return length
    pass
  

  def CreateObstacle(self):
    Obstacle_number=3+0.1*(pygame.time.get_ticks()-MainGame.starttime)/1000
    #Obstacle_number=1
    if len(MainGame.objectgroup)>=math.floor(Obstacle_number):
      return
    pos=random.randint(0,WINDOW_WIDTH),random.randint(0,WINDOW_HEIGHT)
    pos=list(pos)
    v_t=random.randint(20,90),random.randint(20,90)
    v_t=list(v_t)
    if random.randint(0,1):
      v_t[0]=-v_t[0]
    if random.randint(0,1):
      v_t[1]=-v_t[1]
      
    #在边界生成子弹
    flag=random.randint(0,3)
    if flag==0:
      pos[0]=0-50
    if flag==1:
      pos[0]=WINDOW_WIDTH
    if flag==2:
      pos[1]=0-80
    if flag==3:
      pos[1]=WINDOW_HEIGHT
    MainGame.objectgroup.add(Obstacle(pos=pos,v=v_t))
    
    pass
  def CreateShoot(self):
    print("shootbulltin")
    # if self.plane.direction==0:
    self.shootgroup.add(ShootBulltin(self.plane.GetPos(),self.plane.direction))
    # if self.plane.direction==1:
    #   self.shootgroup.add(ShootBulltin(self.plane.GetPos(),self.plane.direction))
      
      
#运行程序
MainGame().run()
  