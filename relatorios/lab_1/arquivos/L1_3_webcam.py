import numpy as np
import cv2 as cv

cap = cv.VideoCapture(2)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
    
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    # Display the resulting frame
    cv.imshow('frame', frame)
    
    key = cv.waitKey(1)
    
    # Save then frame when 'x' is pressed
    if key == ord('x'):
        cv.imwrite('foto1.png', frame)
        print("Frame saved as 'foto1.png'")
        
    # Break the loop when 'q' is pressed
    if key == ord('q'):
        print("Exiting...")
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()