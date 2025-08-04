
## Relatório Laboratório 5 – Extração de Características (Features)

**ESZA019 – Visão Computacional**

**Membros do grupo:**
> - Ian Victor Toniolo Silva - 11202020351
> - Cesar Seiji Maruyama - 11127015
> - Pedro Henrique Cardoso Silva - 11202021250
> - Guilherme de Sousa Santos - 11201921175

**Data de realização dos experimentos:**
- 02/07/2025 (quarta-feira)

**Data de publicação do relatório:**
- 21/07/2025 (segunda-feira)

---

## 1. Introdução

Neste relatório, abordamos os conceitos de extração de características (features) em Visão Computacional, com foco em técnicas de detecção, descrição e correspondência de pontos-chave em imagens. São apresentados experimentos práticos utilizando algoritmos clássicos como Harris, Shi-Tomasi e SIFT, além de aplicações de homografia e transformada de Hough. O objetivo é compreender como essas técnicas podem ser utilizadas para identificar objetos e padrões em imagens, tanto estáticas quanto em vídeo, e discutir suas aplicações em projetos práticos.

### 1.1. Estudo da Teoria

#### O que são Features?
Features são pontos, regiões ou padrões em uma imagem que possuem propriedades distintas e podem ser detectados e descritos de forma robusta. Elas são fundamentais para tarefas como reconhecimento de objetos, rastreamento e reconstrução 3D. [Referência](https://docs.opencv.org/4.x/df/d54/tutorial_py_features_meaning.html)

#### Detector de Harris
O detector de Harris identifica cantos em imagens, que são regiões com variação significativa de intensidade em múltiplas direções. É eficiente para encontrar pontos de interesse, mas não é invariante à escala. [Referência](https://docs.opencv.org/4.x/dc/d0d/tutorial_py_features_harris.html)

#### Detector de Shi-Tomasi
O método Shi-Tomasi aprimora o Harris, selecionando os melhores cantos com base em um critério de qualidade, sendo amplamente utilizado em rastreamento de pontos. [Referência](https://docs.opencv.org/4.x/d4/d8c/tutorial_py_shi_tomasi.html)

#### SIFT (Scale-Invariant Feature Transform)
O SIFT detecta e descreve pontos-chave invariantes à escala e rotação, permitindo encontrar correspondências entre imagens mesmo sob diferentes condições. É uma das técnicas mais robustas para detecção e descrição de features. [Referência](https://docs.opencv.org/4.x/da/df5/tutorial_py_sift_intro.html)

---

## 2. Procedimentos Experimentais

### 2.1. Configuração do Ambiente

Instale as bibliotecas necessárias:
```bash
pip install opencv-python opencv-python-headless numpy matplotlib
```

### 2.2. Captura de Imagens com a Webcam

Utilize o código `capture_image.py` para capturar imagens da webcam. Salve uma imagem do objeto isolado (`object.png`) e outra do objeto na cena (`object_in_scene.png`).

#### Exemplos:
**Objeto:**
<img src="parte_2/object.png">

**Objeto na cena:**
<img src="parte_2/object_in_scene.png">

### 2.3. Feature Matching + Homography (SIFT)

O código `parte_2/feature_matching.py` realiza a correspondência de características entre as duas imagens usando SIFT e FLANN, aplicando homografia para localizar o objeto na cena.

**Etapas do código:**
1. Carregar as imagens.
2. Detectar e computar os descritores com SIFT.
3. Encontrar correspondências com FLANN.
4. Aplicar o teste de razão de Lowe.
5. Calcular a homografia.
6. Desenhar o polígono de correspondência.

Execute com:
```bash
python3 parte_2/feature_matching.py
```
Resultado esperado:
<img src="parte_2/result.png">

### 2.4. Feature Matching em Vídeo Estereoscópico

Para realizar a correspondência de características em tempo real usando duas webcams da câmera estereoscópica calibrada, modifique o código para capturar frames simultaneamente das duas câmeras e aplicar o mesmo processo de detecção e correspondência. Exemplo de estrutura:

```python
import cv2

cap_left = cv2.VideoCapture(0)
cap_right = cv2.VideoCapture(1)

sift = cv2.SIFT_create()
flann = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=50))

while True:
    ret_l, frame_l = cap_left.read()
    ret_r, frame_r = cap_right.read()
    if not ret_l or not ret_r:
        break
    kp1, des1 = sift.detectAndCompute(frame_l, None)
    kp2, des2 = sift.detectAndCompute(frame_r, None)
    matches = flann.knnMatch(des1, des2, k=2)
    good = []
    for m, n in matches:
        if m.distance < 0.7 * n.distance:
            good.append(m)
    result = cv2.drawMatches(frame_l, kp1, frame_r, kp2, good, None, flags=2)
    cv2.imshow('Stereo Feature Matching', result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap_left.release()
cap_right.release()
cv2.destroyAllWindows()
```

---

## 3. Hough Transform

### 3.1. Detecção de Linhas e Círculos em Imagens

Utilize o código `parte_3/hough_transform.py` para detectar linhas e círculos em imagens gravadas, conforme tutorial [LearnOpenCV](https://learnopencv.com/hough-transform-with-opencv-c-python/).

**Exemplo de código para círculos:**
```python
import cv2
import numpy as np

img = cv2.imread('parte_3/circulos.png', 0)
img_color = cv2.imread('parte_3/circulos.png')
img_blur = cv2.medianBlur(img, 5)
circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, 20,
                           param1=50, param2=30, minRadius=0, maxRadius=0)
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv2.circle(img_color, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv2.circle(img_color, (i[0], i[1]), 2, (0, 0, 255), 3)
cv2.imshow('detected circles', img_color)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

**Exemplo de código para linhas:**
```python
img = cv2.imread('parte_3/circulos1.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
cv2.imshow('detected lines', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### 3.2. Hough Transform em Vídeo Estereoscópico

Modifique o código para capturar frames das duas webcams e aplicar a detecção de linhas e círculos em tempo real, exibindo os resultados lado a lado.

---

## 4. Análise e Discussão dos Estudos Realizados

As técnicas de detecção e descrição de features são essenciais em Visão Computacional, permitindo identificar e rastrear objetos em diferentes condições. O uso de SIFT e FLANN mostrou-se eficiente para encontrar correspondências robustas entre imagens, enquanto a homografia possibilita localizar objetos mesmo sob transformações geométricas. A transformada de Hough é fundamental para detectar formas geométricas simples, como linhas e círculos, sendo útil em aplicações industriais e robóticas.

No contexto do trabalho T1, essas técnicas podem ser aplicadas para reconhecimento de objetos, navegação autônoma, reconstrução 3D e análise de cenas, aumentando a precisão e robustez dos sistemas desenvolvidos.

---

## 5. Conclusões

O laboratório permitiu compreender e aplicar os principais métodos de extração e correspondência de características em imagens e vídeo. A integração dessas técnicas é fundamental para o desenvolvimento de sistemas inteligentes de visão computacional, com aplicações em diversas áreas, como robótica, automação, segurança e análise de imagens.

---

## 6. Referências Consultadas e Indicadas

- [Feature Detection and Description - OpenCV](https://docs.opencv.org/4.x/db/d27/tutorial_py_table_of_contents_feature2d.html)
- [Entendendo sobre Features](https://docs.opencv.org/4.x/df/d54/tutorial_py_features_meaning.html)
- [Detector de Harris](https://docs.opencv.org/4.x/dc/d0d/tutorial_py_features_harris.html)
- [Detector de Shi-Tomasi](https://docs.opencv.org/4.x/d4/d8c/tutorial_py_shi_tomasi.html)
- [Introdução ao SIFT](https://docs.opencv.org/4.x/da/df5/tutorial_py_sift_intro.html)
- [Feature Matching + Homography](https://docs.opencv.org/4.x/d1/de0/tutorial_py_feature_homography.html)
- [Hough Transform - LearnOpenCV](https://learnopencv.com/hough-transform-with-opencv-c-python/)

---