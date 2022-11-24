import cv2
import time
import handTrackingVishModule as htm
import json


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)



pTime = 0
detector = htm.handDetector(detectionCon=0.75)

#used to locate finger tips
tipIds = [4, 8, 12, 16, 20]

openTime = time.time()


while cap.isOpened():
    success, img = cap.read()

    if success:

        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        # print(lmList)

        if len(lmList) != 0:
            fingers = []

            

            # 4 Fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            # print(fingers)
            totalFingers = fingers.count(1)
            print(totalFingers)

            #cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                        10, (255, 0, 0), 25)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                    3, (255, 0, 0), 3)

        with open('data.json') as f:
            data = json.load(f)
            question = (data['question'])
            options = (data['options'])
            answer = (data[ 'answer'])

        

        for num in range(len(question)):
            cuTime = time.time()
            if((cuTime - openTime) > 5):
                #img = cap.read()
                cv2.putText(img, f'Question: {str(question[num])}', (40, 70), cv2.FONT_HERSHEY_PLAIN,
                        1, (255, 0, 0), 1)
                cv2.putText(img, f'Options: {str(options[num])}', (40, 150), cv2.FONT_HERSHEY_PLAIN,
                        1, (255, 0, 0), 1)

                break

        
            

        cv2.imshow("Result", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def answerCapture(fingercount):
    varFing = 0
    if(fingercount == varFing):
        time.sleep(2000)
        if(fingercount == varFing):
            return True
        else:
            return False