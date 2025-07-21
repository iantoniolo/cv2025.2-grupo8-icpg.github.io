import numpy as np
import cv2

# IDs dos vídeos de entrada
CamL_id = "data-lab/stereoR.mp4"
CamR_id = "data-lab/stereoL.mp4"

CamL = cv2.VideoCapture(CamL_id)
CamR = cv2.VideoCapture(CamR_id)

print("Reading parameters ......")
cv_file = cv2.FileStorage("improved_params2.xml", cv2.FILE_STORAGE_READ)

Left_Stereo_Map_x = cv_file.getNode("Left_Stereo_Map_x").mat()
Left_Stereo_Map_y = cv_file.getNode("Left_Stereo_Map_y").mat()
Right_Stereo_Map_x = cv_file.getNode("Right_Stereo_Map_x").mat()
Right_Stereo_Map_y = cv_file.getNode("Right_Stereo_Map_y").mat()
cv_file.release()

output_video = cv2.VideoWriter('3d_output_video.mp4', 
                               cv2.VideoWriter_fourcc(*'mp4v'),
                               30, 
                               (700, 700))

while True:
    retR, imgR = CamR.read()
    retL, imgL = CamL.read()
    
    if retL and retR:
        imgR_gray = cv2.cvtColor(imgR, cv2.COLOR_BGR2GRAY)
        imgL_gray = cv2.cvtColor(imgL, cv2.COLOR_BGR2GRAY)

        Left_nice = cv2.remap(imgL, Left_Stereo_Map_x, Left_Stereo_Map_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
        Right_nice = cv2.remap(imgR, Right_Stereo_Map_x, Right_Stereo_Map_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

        output = Right_nice.copy()
        output[:, :, 0] = Right_nice[:, :, 0]
        output[:, :, 1] = Right_nice[:, :, 1]
        output[:, :, 2] = Left_nice[:, :, 2]

        output = cv2.resize(output, (700, 700))

        cv2.namedWindow("3D movie", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("3D movie", 700, 700)
        cv2.imshow("3D movie", output)

        output_video.write(output)

        cv2.waitKey(1)
    else:
        break

# Libera os recursos quando o loop termina
CamL.release()
CamR.release()
output_video.release()
cv2.destroyAllWindows()

print("Vídeo 3D gravado com sucesso como '3d_output_video.mp4'!")
