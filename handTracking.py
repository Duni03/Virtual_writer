import cv2
import mediapipe as mp
import time

class handdetect():
    def __init__(self,mode=False,maxhands=2,detectconf=0.5,trackconf=.5):
        self.mode=mode
        self.maxhands=maxhands
        self.detectconf=detectconf
        self.trackconf=trackconf

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode, self.maxhands,self.detectconf,self.trackconf)
        self.mpDraw=mp.solutions.drawing_utils

    def findhand(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.res= self.hands.process(imgRGB)
        #print(res.multi_hand_landmarks)
        if self.res.multi_hand_landmarks:
            for self.handys in self.res.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,self.handys, self.mphands.HAND_CONNECTIONS)
                
        return img     
    def findpos(self,img,handno=0,draw=True):
        listu=[]

        if self.res.multi_hand_landmarks:

            myhand = self.res.multi_hand_landmarks[0]
            for id,lm in enumerate(self.handys.landmark):
                #print(id,lm)
                h,w,c = img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
                listu.append([id,cx,cy])
                ### DRAW need to used but u did not write it check pls
                #print(id,cx,cy)
        return listu

def main():
    ptime=0
    ctime=0

    cap = cv2.VideoCapture(0)

    detect=handdetect()
    while True:
        val, img = cap.read()

        img = detect.findhand(img)

        img = cv2.flip(img, 1)

        l = detect.findpos(img)

        if len(l)!=0:
            print(l[4],l[8])

        ########
        ctime=time.time()
        fps=1/(ctime-ptime)
        ptime=ctime
        cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255,3),2)
        ########
        
        cv2.imshow("image",img)
        if cv2.waitKey(10) and 0xff==ord('d'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()