import cv2
import numpy as np
import module.hand_tracking_module as htm
import time
import autopy

###################

wCam, hCam = 520, 370
frameR_h = 160  # Frame Reduction
frameR_w = 90
smoothening = 8

#########################



def main_avm(queue_shared):

    pTime = 0
    detector = htm.HandDetector(maxHands=1)
    wScr, hScr = autopy.screen.size()
    
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    cap = cv2.VideoCapture(0)
    cap.set(9, wCam)
    cap.set(11, hCam)

    i = 0
    while True:
        
        #  Find hand Landmarks
        success, img_org = cap.read()
        width = int(cap.get(3))
        height = int(cap.get(4))

        img = cv2.resize(img_org, (0,0), fx = 0.7, fy = 0.7)
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
       
        #  Get the tip of the index and middle fingers
        if len(lmlist) != 0:

            x1, y1 = lmlist[8][1:]

            # Check which fingers are up
            fingers = detector.fingersUp()

            cv2.rectangle(img, (frameR_w, frameR_h), (wCam - frameR_w, hCam - frameR_h), (255, 0, 255), 2)


            #  Only Index Finger : Moving Mode
            if fingers[1] == 1 and fingers[2] == 0:
            
            # 5. Convert Coordinates
                x3 = np.interp(x1, (frameR_w, wCam - frameR_w), (0, wScr))
                y3 = np.interp(y1, (frameR_h, hCam - frameR_h), (0, hScr))
                # Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                
                # Move Mouse
                try:
                    autopy.mouse.move(wScr - clocX, clocY)
                except:
                    pass
                circle_img =  cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                
                plocX, plocY = clocX, clocY

            else:
                i += 1
                # print("Index finger not found",i)
                queue_shared.put(0)


        #  Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        
        #  Display
        # cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main_avm()


