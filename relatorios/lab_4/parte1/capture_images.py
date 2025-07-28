import numpy as np
import cv2
import time

print("Checking the right and left camera IDs:")
print("Press (y) if IDs are correct and (n) to swap the IDs")
print("Press enter to start the process >> ")
input()

# Check for left and right camera IDs
CamL_id = 2
CamR_id = 0

CamL = cv2.VideoCapture(CamL_id)
CamR = cv2.VideoCapture(CamR_id)

for i in range(100):
    retL, frameL = CamL.read()
    retR, frameR = CamR.read()

cv2.imshow('imgL', frameL)
cv2.imshow('imgR', frameR)

key = cv2.waitKey(0)
if key & 0xFF in [ord('y'), ord('Y')]:
    CamL_id = 0
    CamR_id = 2
    print("Camera IDs maintained")
elif key & 0xFF in [ord('n'), ord('N')]:
    CamL_id = 2
    CamR_id = 0
    print("Camera IDs swapped")
else:
    print("Wrong input response")
    exit(-1)

CamR.release()
CamL.release()

CamL = cv2.VideoCapture(CamL_id)
CamR = cv2.VideoCapture(CamR_id)
output_path = "./data/"
start = time.time()
T = 1
count = 0

while True:
    timer = T - int(time.time() - start)
    retR, frameR = CamR.read()
    retL, frameL = CamL.read()
    
    grayR = cv2.cvtColor(frameR, cv2.COLOR_BGR2GRAY)
    grayL = cv2.cvtColor(frameL, cv2.COLOR_BGR2GRAY)

    retR, cornersR = cv2.findChessboardCorners(grayR, (6,8), None)
    retL, cornersL = cv2.findChessboardCorners(grayL, (6,8), None)

    print(retR, retL, timer)

    # Draw corners in real-time for visual feedback
    # if retR:
    #     cv2.drawChessboardCorners(frameR, (6,8), cornersR, retR)
    # if retL:
    #     cv2.drawChessboardCorners(frameL, (6,8), cornersL, retL)

    # Overlay countdown
    # cv2.putText(frameL, "%r" % timer, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (55,0,0), 3)

    # Display images
    cv2.imshow('imgR', frameR)
    cv2.imshow('imgL', frameL)

    # Save frames if corners are detected and timer is zero
    if retR and retL and timer <= 0:
        count += 1
        cv2.imwrite(output_path + 'stereoR/img%d.png' % count, frameR)
        cv2.imwrite(output_path + 'stereoL/img%d.png' % count, frameL)

    if timer <= 0:
        start = time.time()

    # Exit on ESC key
    if cv2.waitKey(1) & 0xFF == 27:
        print("Closing the cameras!")
        break

CamR.release()
CamL.release()
cv2.destroyAllWindows()
