from func import Get_Distance,Get_Angle
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
    self.left_fingers=None
    self.right_fingers=None
    self.clcik_count=0
    self.event_count=0
    self.old_event_count=0
    
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
    self.left_fingers=self.Get_Fingers(hand_orientaion='Left')
    self.right_fingers=self.Get_Fingers(hand_orientaion='Right')
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
  
  def Get_Fingers(self,hand_orientaion,position=None):
    fingers=[]
    #print(position)
    if position==None:
      position=self.position
    
    #判断拇指
    tip=position[hand_orientaion].get(4,None)
    mid=position[hand_orientaion].get(5,None)
    if(tip==None or mid==None):
        return None
    if tip[1]<mid[1]:
        fingers.append(1)
        
    else:
      fingers.append(0)

    #判断食指
    for i in range(2, 6):
      tip=position[hand_orientaion].get(i*4,None)
      mid=position[hand_orientaion].get(i*4-2,None)
      if(tip==None or mid==None):
        return None
      if tip[1]<mid[1]:
        fingers.append(1)
      else:
        fingers.append(0)
    return fingers
  
  def isleft(self):
    tip2=self.position['Left'].get(8,None)
    knot2=self.position['Left'].get(5,None)
    tip3=self.position['Left'].get(12,None)
    knot3=self.position['Left'].get(9,None)
    tip1=self.position['Left'].get(4,None)
    knot1=self.position['Left'].get(2,None)
    if(tip2==None or knot2==None):
        return False

    if tip2[0]>knot2[0]:
      _,angle=Get_Angle(knot2,tip2,(1,0))
      if angle<10:
        #判断其他手指状况
        if Get_Distance(tip2,knot2)/2<Get_Distance(tip2,tip3) and Get_Distance(tip2,knot2)/2<Get_Distance(tip1,tip2):
          self.event_count+=1
          if self.event_count>=3:
              self.event_count=0
              return True
          return False
    
    
    #self.event_count=0
    return False
    pass
  def isright(self):
    tip2=self.position['Right'].get(8,None)
    knot2=self.position['Right'].get(5,None)
    tip3=self.position['Right'].get(12,None)
    knot3=self.position['Right'].get(9,None)
    tip1=self.position['Right'].get(4,None)
    knot1=self.position['Right'].get(2,None)
    if(tip2==None or knot2==None):
        return False

    if tip2[0]<knot2[0]:
      _,angle=Get_Angle(knot2,tip2,(1,0))
      if angle<10:
        #判断其他手指状况
        if Get_Distance(tip2,knot2)/2<Get_Distance(tip2,tip3) and Get_Distance(tip2,knot2)/2<Get_Distance(tip1,tip2):
          self.event_count+=1
          if self.event_count>=3:
              self.event_count=0
              return True
          return False
    
    return False
          
  def isup(self)->bool:

    fingers_list=[]
    directions=[]
    if self.left_fingers!=None:
      fingers_list.append(self.left_fingers)
      directions.append('Left')
    if self.right_fingers!=None:
      fingers_list.append(self.right_fingers)
      directions.append('Right')
    if len(fingers_list)==0:
      return False
    
    for fingers,direction in zip(fingers_list,directions):
      if fingers[1]==1 and fingers[2]==0 and fingers[3]==0 and fingers[4]==0:
        tip2=self.position[direction].get(8,None)
        knot2=self.position[direction].get(5,None)
        if tip2[1]<knot2[1]:
          _,angle_t=Get_Angle(knot2,tip2,(0,1))
          if abs(angle_t)<20:
            self.event_count+=1
            if self.event_count>=3:
              self.event_count=0
              return True
            return False
        
        

    return False
    pass
  
  def isdown(self):
    fingers_list=[]
    directions=[]
    if self.left_fingers!=None:
      fingers_list.append(self.left_fingers)
      directions.append('Left')
    if self.right_fingers!=None:
      fingers_list.append(self.right_fingers)
      directions.append('Right')
    if len(fingers_list)==0:
      return False
    
    for fingers,direction in zip(fingers_list,directions):
        tip2=self.position[direction].get(8,None)
        knot2=self.position[direction].get(5,None)
        if tip2[1]>knot2[1]:
          _,angle_t=Get_Angle(knot2,tip2,(0,-1))
          if abs(angle_t)<20:
            self.event_count+=1
            if self.event_count>=3:
              self.event_count=0
              return True
            return False
        
    #确保isdown最后
    if self.event_count==self.old_event_count:
      self.event_count=0
    self.old_event_count=self.event_count
    return False
    
  def click(self)->bool:
    #print(fingers)
    fingers_list=[]
    directions=[]
    if self.left_fingers!=None:
      fingers_list.append(self.left_fingers)
      directions.append('Left')
    if self.right_fingers!=None:
      fingers_list.append(self.right_fingers)
      directions.append('Right')
      
    if len(fingers_list)==0:
      return False

    for fingers,direction in zip(fingers_list,directions):
      
      if fingers[1]==1 and fingers[2]==1:
        tip2=self.position[direction].get(8,None)
        tip3=self.position[direction].get(12,None)
        mid3=self.position[direction].get(10,None)
        _,angle_t=Get_Angle(mid3,tip3,(0,1))
        if abs(angle_t)<20:
          if Get_Distance(tip2,tip3)<Get_Distance(tip3,mid3):
            
          #if abs(Get_Angle()):
            self.clcik_count+=1
            if self.clcik_count>=3:
              self.clcik_count=0
              return True
            return False
    self.clcik_count=0
    return False