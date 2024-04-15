import math

def Get_Distance(p1, p2):
  x1, y1 = p1
  x2, y2 = p2
  length = math.hypot(x2 - x1, y2 - y1)
  return length

def Get_Angle(p1,p2,v):
  flag=True
  x1,y1=p1
  x2,y2=p2
  px, py = x2-x1,y2-y1
  vx,vy=v
  angle1 = math.atan2(py, px)
  angle1=math.degrees(angle1)
  angle2= math.atan2(vy, vx)
  angle2=math.degrees(angle2)
  angle=abs(angle2-angle1)
  if angle>90:
    angle=180-angle
    flag=False
  #print(flag)
  return flag,angle




#Get_Angle((2,1),(-1,1))