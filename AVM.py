import cv2
import numpy as np
import HandTrackingMod as htm
import time
import autopy

##########################
wCam, hCam = 520, 270
frameR = 50  # Frame Reduction
smoothening = 8
#########################



def main_avm():

    pTime = 0
    detector = htm.HandDetector(maxHands=1)
    wScr, hScr = autopy.screen.size()
    #print(wScr, hScr)
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    cap = cv2.VideoCapture(0)
    cap.set(9, wCam)
    cap.set(11, hCam)

    while True:
        # 1. Find hand Landmarks
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist, bbox = detector.findPosition(img)
        #print("AVM lmlist:", detector.lmlist)

        # 2. Get the tip of the index and middle fingers
        if len(lmlist) != 0:
            x1, y1 = lmlist[8][1:]
            #x2, y2 = lmlist[12][1:]
            #print(x1, y1, x2, y2)

            #3. Check which fingers are up
            fingers = detector.fingersUp()
            #print(fingers)

            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)


            # 4. Only Index Finger : Moving Mode
            if fingers[1] == 1 and fingers[2] == 0:
            # 5. Convert Coordinates
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                # 6. Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening
                # 7. Move Mouse
                autopy.mouse.move(wScr - clocX, clocY)
                #autopy.mouse.move(wScr - x3, y3)
                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY

            """
            # 8. Both Index and middle fingers are up : Clicking Mode
            if fingers[1] == 1 and fingers[2] == 1:
                # 9. Find distance between fingers
                length, img, lineInfo = detector.findDistance(8, 12, img)

                if length < 40:
                    pass
                #print(length)
                
                # 10. Click mouse if distance short
                if length < 40:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                    #autopy.mouse.click()
                    break
                """
            
            

        # 11. Frame Rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        # 12. Display
        cv2.imshow("Image", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        #if length < 40:
            #break
    return x1, y1

    cv2.destroyAllWindows()

    

if __name__ == "__main__":
    main_avm()


