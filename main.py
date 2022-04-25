from cvzone.HandTrackingModule import HandDetector
import cv2
import socket

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
success, img = cap.read()
h, w, _ = img.shape
h1, w1, _ = img.shape
detector = HandDetector(detectionCon=0.8, maxHands=2)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.1", 5052)
serverAddressPort2 = ("127.0.0.1", 5051)

while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw
    data = []
    data1 = []

    if hands:
        # Hand 1
        hand = hands[0]
        lmList = hand["lmList"]  # List of 21 Landmark points
        for lm in lmList:
            data.extend([lm[0], h - lm[1], lm[2]])

        sock.sendto(str.encode(str(data)), serverAddressPort)

        if len(hands) >= 2:
            hand1 = hands[1]
            lmList1 = hand1["lmList"]  # List of 21 Landmark points
            for lm1 in lmList1:
                data1.extend([lm1[0], h1 - lm1[1], lm1[2]])
            sock.sendto(str.encode(str(data1)), serverAddressPort2)

    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)