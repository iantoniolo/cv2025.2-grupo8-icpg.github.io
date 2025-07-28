import numpy as np 
import cv2
from tqdm import tqdm
# Set the path to the images captured by the left and right cameras
pathL = "./data/stereoL/"
pathR = "./data/stereoR/"
 
# Termination criteria for refining the detected corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
 
objp = np.zeros((8*6,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)
 
img_ptsL = []
img_ptsR = []
obj_pts = []
 
for i in tqdm(range(1,10)):
 imgL = cv2.imread(pathL+"img%d.png"%i)
 imgR = cv2.imread(pathR+"img%d.png"%i)
 imgL_gray = cv2.imread(pathL+"img%d.png"%i,0)
 imgR_gray = cv2.imread(pathR+"img%d.png"%i,0)

 print(f"imageL {imgL} imageR {imgR}")
 
 outputL = imgL.copy()
 outputR = imgR.copy()
 
 retR, cornersR =  cv2.findChessboardCorners(outputR,(8,6),None)
 retL, cornersL = cv2.findChessboardCorners(outputL,(8,6),None)
 
 if retR and retL:
  obj_pts.append(objp)
  cv2.cornerSubPix(imgR_gray,cornersR,(11,11),(-1,-1),criteria)
  cv2.cornerSubPix(imgL_gray,cornersL,(11,11),(-1,-1),criteria)
  cv2.drawChessboardCorners(outputR,(8,6),cornersR,retR)
  cv2.drawChessboardCorners(outputL,(8,6),cornersL,retL)
  cv2.imshow('cornersR',outputR)
  cv2.imshow('cornersL',outputL)
  cv2.waitKey(0)
 
  img_ptsL.append(cornersL)
  img_ptsR.append(cornersR)
 
# print("Image chessboard corners (left):", img_ptsL)
# print("Image chessboard corners (right):", img_ptsR)

# Calibrating left camera
retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(obj_pts,img_ptsL,imgL_gray.shape[::-1],None,None)
# print("Camera matrix (left):", mtxL)
# print("Distortion coefficients (left):", distL)
# print("Rotation vectors (left):", rvecsL)
# print("Translation vectors (left):", tvecsL)

hL,wL= imgL_gray.shape[:2]
new_mtxL, roiL= cv2.getOptimalNewCameraMatrix(mtxL,distL,(wL,hL),1,(wL,hL))
 
# Calibrating right camera
retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(obj_pts,img_ptsR,imgR_gray.shape[::-1],None,None)
# print("Camera matrix (right):", mtxR)
# print("Distortion coefficients (right):", distR)
# print("Rotation vectors (right):", rvecsR)
# print("Translation vectors (right):", tvecsR)

hR,wR= imgR_gray.shape[:2]
new_mtxR, roiR= cv2.getOptimalNewCameraMatrix(mtxR,distR,(wR,hR),1,(wR,hR))

flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC
# Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
# Hence intrinsic parameters are the same 
 
criteria_stereo= (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
 
 
# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retS, new_mtxL, distL, new_mtxR, distR, Rot, Trns, Emat, Fmat = cv2.stereoCalibrate(obj_pts, img_ptsL, img_ptsR, new_mtxL, distL, new_mtxR, distR, imgL_gray.shape[::-1], criteria_stereo, flags)

# print("Stereo calibration successful:", retS)
# print("New camera matrix (left):", new_mtxL)
# print("New camera matrix (right):", new_mtxR)
# print("Distortion coefficients (left):", distL)
# print("Distortion coefficients (right):", distR)
# print("Rotation matrix:", Rot)
# print("Translation vector:", Trns)
# print("Essential matrix:", Emat)
# print("Fundamental matrix:", Fmat)

rectify_scale= 0
rect_l, rect_r, proj_mat_l, proj_mat_r, Q, roiL, roiR= cv2.stereoRectify(new_mtxL, distL, new_mtxR, distR, imgL_gray.shape[::-1], Rot, Trns, rectify_scale,(0,0))

print("Rectification transformation (left):", rect_l)
print("Rectification transformation (right):", rect_r)
print("Projection matrix (left):", proj_mat_l)
print("Projection matrix (right):", proj_mat_r)
print("Disparity-to-depth mapping matrix Q:", Q)
print("ROI (left):", roiL)
print("ROI (right):", roiR)

Left_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxL, distL, rect_l, proj_mat_l,
                                             imgL_gray.shape[::-1], cv2.CV_16SC2)
Right_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxR, distR, rect_r, proj_mat_r,
                                              imgR_gray.shape[::-1], cv2.CV_16SC2)
 
print("Left Stereo Map:", Left_Stereo_Map)
print("Right Stereo Map:", Right_Stereo_Map)
 
print("Saving paraeters ......")
cv_file = cv2.FileStorage("./data/params_py.xml", cv2.FILE_STORAGE_WRITE)
cv_file.write("Left_Stereo_Map_x",Left_Stereo_Map[0])
cv_file.write("Left_Stereo_Map_y",Left_Stereo_Map[1])
cv_file.write("Right_Stereo_Map_x",Right_Stereo_Map[0])
cv_file.write("Right_Stereo_Map_y",Right_Stereo_Map[1])
cv_file.release()