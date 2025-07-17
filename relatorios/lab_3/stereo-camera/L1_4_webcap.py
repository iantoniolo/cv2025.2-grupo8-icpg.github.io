import numpy as np
import cv2 as cv

# Inicializa as duas webcams
cap1 = cv.VideoCapture(2)  # Primeira webcam
cap2 = cv.VideoCapture(4)  # Segunda webcam

# Obtém as dimensões e configurações da primeira webcam
width1 = int(cap1.get(cv.CAP_PROP_FRAME_WIDTH))
height1 = int(cap1.get(cv.CAP_PROP_FRAME_HEIGHT))
fps1 = 60.0

# Obtém as dimensões e configurações da segunda webcam
width2 = int(cap2.get(cv.CAP_PROP_FRAME_WIDTH))
height2 = int(cap2.get(cv.CAP_PROP_FRAME_HEIGHT))
fps2 = 60.0

# Define o codec e cria os objetos VideoWriter para ambas as webcams
fourcc = cv.VideoWriter_fourcc(*'XVID')
out1 = cv.VideoWriter('saida_cam1.avi', fourcc, fps1, (width1, height1))
out2 = cv.VideoWriter('saida_cam2.avi', fourcc, fps2, (width2, height2))

while cap1.isOpened() and cap2.isOpened():
    # Lê os frames de ambas as webcams
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        print("Não foi possível receber frames (fim do stream?). Saindo...")
        break

    # Escreve os frames capturados nos arquivos de saída
    out1.write(frame1)
    out2.write(frame2)

    # Mostra os frames capturados em janelas separadas
    cv.imshow('Webcam 1', frame1)
    cv.imshow('Webcam 2', frame2)

    # Pressione 'q' para sair
    if cv.waitKey(1) == ord('q'):
        break

# Libera todos os recursos ao finalizar
cap1.release()
cap2.release()
out1.release()
out2.release()
cv.destroyAllWindows()