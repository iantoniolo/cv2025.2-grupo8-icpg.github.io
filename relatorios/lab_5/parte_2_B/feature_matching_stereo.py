import cv2
import numpy as np

cap_left = cv2.VideoCapture(0) 
cap_right = cv2.VideoCapture(2)

if not cap_left.isOpened() or not cap_right.isOpened():
    print("Erro ao abrir as câmeras!")
    exit()

sift = cv2.SIFT_create()

bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)

while True:
    ret_left, frame_left = cap_left.read()
    ret_right, frame_right = cap_right.read()

    if not ret_left or not ret_right:
        print("Erro ao capturar imagem!")
        break

    gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

    kp_left, des_left = sift.detectAndCompute(gray_left, None)
    kp_right, des_right = sift.detectAndCompute(gray_right, None)

    matches = bf.match(des_left, des_right)

    matches = sorted(matches, key=lambda x: x.distance)

    match_img = cv2.drawMatches(frame_left, kp_left, frame_right, kp_right, matches[:50], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

    cv2.imshow('Feature Matching', match_img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap_left.release()
cap_right.release()
cv2.destroyAllWindows()
