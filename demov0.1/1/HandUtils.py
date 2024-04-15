from func import Get_Distance
import mediapipe as mp
import cv2
import numpy as np
import math

def add_alpha_channel(img):
    """ 为jpg图像添加alpha通道 """
 
    b_channel, g_channel, r_channel = cv2.split(img) # 剥离jpg图像通道
    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255 # 创建Alpha通道
 
    img_new = cv2.merge((b_channel, g_channel, r_channel, alpha_channel)) # 融合通道
    return img_new

def BlendImage(background_img,png_img,x,y):
  if background_img.shape[-1]==3:
    background_img=add_alpha_channel(background_img)
  # print(background_img.shape)
  # print(png_img.shape)
  w1,h1=background_img.shape[1::-1]
  w2,h2=png_img.shape[1::-1]
  if (x+w2)>w1: x=w1-w2
  if (y+h2)>h1: y=h1-h2
  alpha_png = png_img[0:h2,0:w2,3] / 255.0
  alpha_jpg = 1 - alpha_png
  for c in range(0,3):
    background_img[y:y+h2, x:x+w2, c] = ((alpha_jpg*background_img[y:y+h2, x:x+w2, c]) + (alpha_png*png_img[0:h2,0:w2,c]))
  return background_img

  
class HandDetector():
  def __init__(self):
    self.hand_detector=mp.solutions.hands.Hands()
    self.drawer=mp.solutions.drawing_utils
    self.position=None
    
  def process(self,img):#寻找关键点
    img_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    self.hand_data=self.hand_detector.process(img_rgb)
    if self.hand_data.multi_hand_landmarks:
      for handlms in self.hand_data.multi_hand_landmarks:
        self.drawer.draw_landmarks(img,handlms,mp.solutions.hands.HAND_CONNECTIONS)
        
  def find_position(self,img):
    h,w,c=img.shape
    position={"Left":{},"Right":{}}
    if self.hand_data.multi_hand_landmarks:
      i=0
      for knot in self.hand_data.multi_handedness:
        score=knot.classification[0].score
        if score>0.8:
          label=knot.classification[0].label
          hand_lms=self.hand_data.multi_hand_landmarks[i].landmark
          for id,lm in enumerate(hand_lms):
            x,y=int(lm.x*w),int(lm.y*h)
            position[label][id]=(x,y)
        i=i+1
    self.position=position
    return position
  
  def Get_Distance(self,p1, p2, img=None):
    x1, y1 = p1
    x2, y2 = p2
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
    length = math.hypot(x2 - x1, y2 - y1)
    info = (x1, y1, x2, y2, cx, cy)
    if img is not None:
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return length,info, img
    else:
        return length, info
    pass
  def Get_Fingers(self,position=None):
    fingers=[]
    #print(position)
    if position==None:
      position=self.position
    
    #判断拇指
    tip=position['Left'].get(4,None)
    mid=position['Left'].get(5,None)
    if(tip==None or mid==None):
        return None
    if tip[1]<mid[1]:
        fingers.append(1)
    else:
      fingers.append(0)

    #判断食指
    for i in range(2, 6):
      tip=position['Left'].get(i*4,None)
      mid=position['Left'].get(i*4-2,None)
      if(tip==None or mid==None):
        return None
      if tip[1]<mid[1]:
        fingers.append(1)
      else:
        fingers.append(0)
    #print(fingers)
    return fingers
  def click(self)->bool:
    fingers=self.Get_Fingers()
    if fingers==None:
      return False
    if fingers[1]==1 and fingers[2]==1:
      tip2=self.position['Left'].get(8,None)
      tip3=self.position['Left'].get(12,None)
      mid3=self.position['Left'].get(10,None)
      if Get_Distance(tip2,tip3)<Get_Distance(tip3,mid3):
        return True
    return False