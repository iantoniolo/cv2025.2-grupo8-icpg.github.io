import cv2
import numpy as np
import glob

# Caminho para as imagens
image_paths = glob.glob("./imagens/*.png")  # Substitua pelo seu diretório

print(f"image_paths {image_paths}")

for path in image_paths:
    print(f"path {path}")
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detecção de bordas
    edges = cv2.Canny(gray, 50, 150)

    # 🟦 Detecção de linhas
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # 🟢 Detecção de círculos
    blurred = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(
    blurred,
    cv2.HOUGH_GRADIENT,
    dp=1.2,                 # Aumenta a precisão dos raios
    minDist=gray.shape[0]//16,  # Distância mínima entre centros
    param1=100,             # Threshold para o Canny
    param2=40,              # Threshold de acumulação (maior = menos círculos)
    minRadius=20,           # Tamanho mínimo dos círculos
    maxRadius=80            # Tamanho máximo dos círculos
)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for c in circles[0, :]:
            cv2.circle(img, (c[0], c[1]), c[2], (0, 255, 0), 2)
            cv2.circle(img, (c[0], c[1]), 2, (0, 0, 255), 3)

    # Mostrar resultado
    cv2.imshow(f"Resultado - {path}", img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
