import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

# Função para detectar câmeras disponíveis
def detect_cameras():
    available_cameras = []
    for i in range(10):  # Tentando até 10 câmeras
        cap = cv.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()  # Liberando a câmera após a detecção
    return available_cameras

# Detectar câmeras disponíveis
# available_cameras = detect_cameras()
# if len(available_cameras) < 2:
#     print("Erro: Duas câmeras não estão disponíveis.")
#     exit()
# else:
#     print(f"Câmeras detectadas: {available_cameras}")

MIN_MATCH_COUNT = 10  # Número mínimo de correspondências para encontrar o objeto

# Inicializar o SIFT
sift = cv.SIFT_create()

# Parâmetros para o FLANN (Fast Library for Approximate Nearest Neighbors)
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

# Inicializar as duas webcams (esquerda e direita)
cap_left = cv.VideoCapture(0)  # Primeira câmera disponível
cap_right = cv.VideoCapture(2)  # Segunda câmera disponível

if not cap_left.isOpened() or not cap_right.isOpened():
    print("Erro ao abrir as webcams.")
    exit()

print("Pressione 'q' para sair.")

while True:
    # Captura dos frames da webcam esquerda e direita
    ret_left, frame_left = cap_left.read()
    ret_right, frame_right = cap_right.read()

    if not ret_left or not ret_right:
        print("Erro ao capturar imagem das webcams.")
        break

    # Convertendo para escala de cinza
    gray_left = cv.cvtColor(frame_left, cv.COLOR_BGR2GRAY)
    gray_right = cv.cvtColor(frame_right, cv.COLOR_BGR2GRAY)

    # Detectando e computando os pontos-chave e descritores
    kp_left, des_left = sift.detectAndCompute(gray_left, None)
    kp_right, des_right = sift.detectAndCompute(gray_right, None)

    # Criando o objeto FLANN Matcher
    flann = cv.FlannBasedMatcher(index_params, search_params)

    # Encontrando as melhores correspondências entre os descritores
    matches = flann.knnMatch(des_left, des_right, k=2)

    # Aplicando o critério de Lowe's ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good_matches.append(m)

    # Se houver boas correspondências, vamos calcular a homografia
    if len(good_matches) > MIN_MATCH_COUNT:
        # Obtendo os pontos das correspondências
        src_pts = np.float32([kp_left[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp_right[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # Calculando a homografia utilizando RANSAC
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
        matchesMask = mask.ravel().tolist()

        # Desenhando o polígono de correspondência na imagem direita
        h, w = gray_left.shape
        pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
        dst = cv.perspectiveTransform(pts, M)

        # Desenhando o polígono
        frame_right = cv.polylines(frame_right, [np.int32(dst)], True, (0, 255, 0), 3, cv.LINE_AA)

    # Desenhando as correspondências
    draw_params = dict(matchColor=(0, 255, 0),  # Correspondências em verde
                       singlePointColor=None,
                       matchesMask=mask.ravel().tolist(),  # Inliers
                       flags=2)

    # Exibindo as correspondências entre as imagens
    img_matches = cv.drawMatches(frame_left, kp_left, frame_right, kp_right, good_matches, None, **draw_params)
    
    # Exibindo o resultado
    cv.imshow("Correspondências Estereoscópicas", img_matches)

    # Verificando se a tecla 'q' foi pressionada para sair
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar as câmeras e fechar as janelas
cap_left.release()
cap_right.release()
cv.destroyAllWindows()
