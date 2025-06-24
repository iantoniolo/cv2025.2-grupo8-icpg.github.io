import time
import numpy as np
import cv2 as cv

cap = cv.VideoCapture('big_buck_bunny.mp4')

while(cap.isOpened()):
    ret, frame = cap.read()
    
    if ret==True:
        # show the frame
        cv.imshow('frame',frame)

        #wait next frame by 40ms - 25fps
        time.sleep(1/25.0) 
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
               
cap.release()
cv.destroyAllWindows()
