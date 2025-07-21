import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

MIN_MATCH_COUNT = 10  # Número mínimo de correspondências para encontrar o objeto

# Carregando as imagens
img1 = cv.imread('object.png', cv.IMREAD_GRAYSCALE)          # Imagem de consulta
img2 = cv.imread('object_in_scene.png', cv.IMREAD_GRAYSCALE) # Imagem de treinamento

# Iniciando o detector SIFT
sift = cv.SIFT_create()

# Detectando e computando os pontos-chave e descritores nas imagens
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# Parâmetros para o FLANN (Fast Library for Approximate Nearest Neighbors)
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

# Criando o objeto FLANN Matcher
flann = cv.FlannBasedMatcher(index_params, search_params)

# Encontrando as melhores correspondências entre os descritores
matches = flann.knnMatch(des1, des2, k=2)

# Aplicando o critério de Lowe's ratio test para selecionar as boas correspondências
good = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good.append(m)

# Condição: se houver pelo menos 10 boas correspondências, procedemos
if len(good) > MIN_MATCH_COUNT:
    # Obtendo os pontos das correspondências em ambas as imagens
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)

    # Calculando a homografia utilizando RANSAC
    M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()

    # Transformando os cantos da imagem de consulta para a imagem de treinamento
    h, w = img1.shape
    pts = np.float32([[0, 0], [0, h-1], [w-1, h-1], [w-1, 0]]).reshape(-1, 1, 2)
    dst = cv.perspectiveTransform(pts, M)

    # Desenhando o polígono da correspondência na imagem de treinamento
    img2 = cv.polylines(img2, [np.int32(dst)], True, 255, 3, cv.LINE_AA)

else:
    print("Não há correspondências suficientes encontradas - {}/{}".format(len(good), MIN_MATCH_COUNT))
    matchesMask = None

# Desenhando as correspondências ou inliers
draw_params = dict(matchColor=(0, 255, 0),  # Desenhando as correspondências em verde
                   singlePointColor=None,
                   matchesMask=matchesMask,  # Desenhando apenas os inliers
                   flags=2)

# Exibindo as correspondências
img3 = cv.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
plt.imshow(img3, 'gray')
plt.show()
