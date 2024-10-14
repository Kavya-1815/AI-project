import cv2
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math
# import pycaw
import mediapipe as mp
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# from video_get import VideoGet


###################

class volume():
    def __init__(self,mode=False, maxHands=1, detectionCon =0.75, minTrackCon = 0.6):
        self.mode= mode
        self.maxHands = maxHands
        self.detectionCon= detectionCon
        self.trackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils
        self.tipIds = [4,8,12,16,20]


    def set_volume(self,img, detector, fingers,cap):
        pTime = 0
        
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        # volume.GetMute()
        # volume.GetMasterVolumeLevel()
        volRange = volume.GetVolumeRange()


        minVol = volRange[0]
        maxVol = volRange[1]
        area = 0

        # video_getter = VideoGet(1).start()
        hands,img = detector.findHands(img)
        if hands:
            fingers = detector.fingersUp(hands[0])

            while fingers[4] == 0:
                success,img = cap.read()
                # img = cv2.flip(img,1)
                hands,img = detector.findHands(img,flipType=False)
                

                if hands:
                    hand = hands[0]
                    bbox = hand["bbox"]
                    area = (bbox[2]*bbox[3])//100
                    lmlist = hand["lmList"]
                    print('volume  ',area)
                    
                    if 180<area<1200:
                        # print('yes')
                        length, img, lineInfo = detector.findDistance(lmlist[4][0:2],lmlist[8][0:2], img)
                        

                        
                        volbar = np.interp(length,[20,210],[400,150])
                        volperc = np.interp(length,[20,210],[0,100])
                        # print(volbar)
                        
                        # volume.SetMasterVolumeLevel(vol, None)
                        #smoothness
                        smoothness = 2
                        volperc = smoothness * round(volperc/smoothness)

                        #check fingers up

                        fingers = detector.fingersUp(hand)
                        
                        # print(fingers)
                        if fingers[0] == 0 and fingers[1]==1 and fingers[4] == 0 and fingers[2]==0 and fingers[3]==0:
                            try:
                                print("Setting volume")
                                volume.SetMasterVolumeLevelScalar(volperc/100,None)
                                
                            except Exception:
                                pass
                        # if len(lmList) == 0:
                        #     break
                    
                    else:
                        print('out of area')

                    # try:
                            
                    #     cv2.rectangle(img, (50,150),(85,400), (255,0,0), 3)
                    #     cv2.rectangle(img, (50, int(volbar)),(85,400), (255,0,0), cv2.FILLED)
                    #     cv2.putText(img, f'{int(volperc)} %', (40,450),cv2.FONT_HERSHEY_COMPLEX, 1,(255,0,0),3)
                    # except Exception:
                    #     pass
                
                if hands == []:
                    print("hands empty")
                    break

                # cVol = int(volume.GetMasterVolumeLevelScalar()*100)
                # cv2.putText(img, f'Vol Set: {int(cVol)}', (400,70), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)

                # cTime=time.time()
                # fps = 1/(cTime-pTime)
                # pTime=cTime

                # cv2.putText(img, f'FPS: {int(fps)}', (40,70), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0),2)

                
                
                # cv2.imshow("Image", img)
                cv2.waitKey(1) 