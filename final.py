import cv2
import mediapipe as mp
import time
import numpy as np
import handTracking as ht
import math

ptime=0
ctime=0

X=[]
Y=[]
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)
cap.set(cv2.CAP_PROP_FPS, 33)


detect=ht.handdetect(maxhands=1,detectconf=0.9)
while True:
    val, img = cap.read()
    img = cv2.flip(img, 1)
    img = detect.findhand(img,draw=False)

    

    l = detect.findpos(img)

    if len(l)!=0:
        #print(l[4],l[8])

        x1,y1 = l[4][1],l[4][2]
        cv2.circle(img,(x1,y1),5,(255,0,0),cv2.FILLED)
        x2,y2 = l[8][1],l[8][2]
        cv2.circle(img,(x2,y2),5,(255,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

        cx,cy=(x1+x2)//2,(y1+y2)//2
        

        le=math.hypot(x1-x2,y1-y2)
        print(le)
        if le<65:
            cv2.circle(img,(cx,cy),10,(0,0,255),cv2.FILLED)
            X.append(cx)
            Y.append(cy)
            #img[cx:cx+50,cy:cy+50]=[0,0,255]
    for i in range(len(X)):
        cv2.circle(img,(X[i],Y[i]),7,(0,0,255),cv2.FILLED)
        cv2.circle(img,(X[i],Y[i]),3,(127, 127, 255),cv2.FILLED)
    ########
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    
    ########
    
    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255,3),2)
    cv2.imshow("image",img)
    if cv2.waitKey(10) and 0xff==ord('d'):
        break
cap.release()
cv2.destroyAllWindows()