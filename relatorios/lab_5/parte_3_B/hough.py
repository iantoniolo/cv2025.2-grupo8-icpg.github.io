import cv2
import numpy as np

# Inicializar as duas webcams (substitua 0 e 1 se necessário)
cam_esquerda = cv2.VideoCapture(0)
cam_direita = cv2.VideoCapture(2)

# Verificar se ambas estão abertas
if not cam_esquerda.isOpened() or not cam_direita.isOpened():
    print("Erro ao abrir as câmeras.")
    exit()

while True:
    retL, frameL = cam_esquerda.read()
    retR, frameR = cam_direita.read()
    
    if not retL or not retR:
        print("Erro ao capturar os frames.")
        break

    def detectar_elementos(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # Detecção de linhas
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=50, maxLineGap=10)
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Detecção de círculos
        blurred = cv2.medianBlur(gray, 5)
        circles = cv2.HoughCircles(
            blurred,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=gray.shape[0]//16,
            param1=100,
            param2=40,
            minRadius=20,
            maxRadius=80
        )
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for c in circles[0, :]:
                cv2.circle(frame, (c[0], c[1]), c[2], (0, 255, 0), 2)
                cv2.circle(frame, (c[0], c[1]), 2, (0, 0, 255), 3)
        
        return frame

    # Aplicar detecção nos dois frames
    processadoL = detectar_elementos(frameL.copy())
    processadoR = detectar_elementos(frameR.copy())

    # Mostrar os dois vídeos lado a lado
    cv2.imshow("Camera Esquerda", processadoL)
    cv2.imshow("Camera Direita", processadoR)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam_esquerda.release()
cam_direita.release()
cv2.destroyAllWindows()
