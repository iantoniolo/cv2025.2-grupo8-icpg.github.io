import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
i = 0
    
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Display the resulting frame
    cv.imshow('frame', frame)

    # Save on "s" key or exit on "q"
    k = cv.waitKey(1) 
    if  k == ord('s'):
        cv.imwrite("frm"+str(i)+".jpg",frame)
        i = i + 1
        print("frame", i)
    elif k == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
