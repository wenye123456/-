from itertools import count
from turtle import left
import pygame
import cv2
import time
from HandUtils import HandDetector
from HandUtils import BlendImage

FPS=120
COUNT=1
item_image=cv2.imread(R"src\mouse.png",cv2.IMREAD_UNCHANGED)
carema=cv2.VideoCapture(0)
hand_detector=HandDetector()
pygame.init()
clock = pygame.time.Clock()
while True:
  starttime=time.time()
  flag,img=carema.read()
  if flag:
    img=cv2.resize(img,(800,600))
    img=cv2.flip(img,1)
    hand_detector.process(img)
    position=hand_detector.find_position(img)
    #hand_detector.Get_Fingers(position)
    right_flag=position['Right'].get(5,None)
    left_finger=position['Left'].get(5,None)
    if left_finger: 
      img=BlendImage(img,item_image,left_finger[0],left_finger[1])
    cv2.imshow("1",img)
    cv2.waitKey(1)
      
  
  clock.tick(FPS)
  endtime=time.time()
  
  #print(endtime-starttime)
