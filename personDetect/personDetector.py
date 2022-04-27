import cv2
from cvzone.PoseModule import PoseDetector
import socket

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
success, img = cap.read()
h, w, _ = img.shape


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)

detector = PoseDetector()
posList = []
while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList, bboxInfo = detector.findPosition(img)
    data = []

    if bboxInfo:
        lmString = ''
        for lm in lmList:
            data.extend([lm[0], h - lm[1], lm[2]])
            lmString += f'{lm[1]},{img.shape[0] - lm[2]},{lm[3]},'
        sock.sendto(str.encode(str(data)), serverAddressPort)
        posList.append(lmString)
    else:
        sock.sendto(str.encode(str(0)), serverAddressPort)
    print(len(posList))

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('s'):
        with open("AnimationFile.txt", 'w') as f:
            f.writelines(["%s\n" % item for item in posList])
