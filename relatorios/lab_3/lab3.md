## Relatório Laboratório 3 – Camera Estéreo

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

### INTRODUÇÃO

TODO: escrever uma intro

#### Objetivos:
- Entender os conceitos de Estereoscopia e Geometria Epipolas.
- Realizar um experimento de Imagem 3D com calibração de câmeras estéreo.
- Elaborar o relatório em equipe de alunos.

### PROCEDIMENTOS EXPERIMENTAIS

#### PARTE 1: Estudo da teoria sobre estereoscopia e parâmetros conjuntos de duas câmeras. Estudar detalhadamente os seguintes itens:

- Estude aqui a geometria epipolar com duas cameras/imagens[2]: <https://learnopencv.com/introduction-to-epipolar-geometry-and-stereo-vision/>.

- Estude aqui a Camera 3D com OpenCV [1]: <https://learnopencv.com/making-a-low-cost-stereo-camera-using-opencv/>

- Atenção: estes exemplos necessitam do óculos 3D anaglifo com lentes nas cores vermelho e ciano.

#### PARTE 2: Executar a construção de uma câmera estereoscopica simples.

i. Seguiremos as instruçoes indicadas na seção “Steps To Create The Stereo Camera Setup” da referencia [1], utilizando duas webcams iguais.

ii. Apoie ambas webcam paralelamente sobre uma superfície plana e firme, de forma que os eixos opticos fiquem aproximadamente 5 cm entre si.

iii. As câmeras não deverão se mover uma em relação à outra após o procedimento de calibração. Portanto, fixe-as fortemente.

iv. No relatório descreva os procedimentos com o máximo de detalhes, de forma a permitir a reprodução do experimento.

#### PARTE 3: Executar passo a passo as etapas do exemplo de calibração de uma câmera estereoscópica e geração de imagem 3D.

(A) Obtenção dos códigos do exemplo da câmera estéreo com OpenCV: Nesta pagina clique no botao “download code” e salve o arquivo numa pasta com seu nome: <https://github.com/spmallick/learnopencv tree/master/stereo-camera>
OBS: ao final da aula no laboratorio apague todos arquivos baixados no computador.
Observe que há tres codigos em python.

(B) Execute o exemplo com as imagens fornecidas:
- Calibração estéreo:
```shell
python3 calibrate.py
```

- Geração e apresentação de imagem 3D
```shell
python3 movie3d.py
```

**Responda: consulte a teoria da calibração e correção de distorção e o exemplo executado, e com isso descreva todos os parametros necessários para a camera estéreo.**

> Para a configuração da câmera estéreo, foi preciso estimar e usar os seguintes parâmetros:
> 1. **Pontos de calibração**: pontos gerados a partir de um padrão de tabuleiro de xadrez.
> 2. **Parâmetros intrínsecos**: para cada câmera individual.
> 3. **Parâmetros extrínsecos**: relacionamento entre as câmeras.
> 4. **Parâmetros de retificação e reprojeção**: para gerar pares de imagens alinhadas e mapear disparidade em profundidade.

**1. Pontos de calibração**

> Os pontos de calibração foram obtidos a partir de um padrão de tabuleiro de xadrez disponível nos arquivos do laboratório. Esses pontos são usados para calcular os parâmetros intrínsecos e extrínsecos das câmeras. Eles foram detectados automaticamente pelo OpenCV usando a função `findChessboardCorners`:

```python
retR, cornersR = cv2.findChessboardCorners(outputR,(8,6),None)
retL, cornersL = cv2.findChessboardCorners(outputL,(8,6),None)
```

**2. Parâmetros intrínsecos**

> Agora que temos os pontos de calibração, podemos calcular os parâmetros intrínsecos de cada câmera separadamente.
> 
> São parâmetros que descrevem as características internas de cada câmera, de modo a fazer uma projeção do mundo 3D para o plano 2D da imagem. Esses parâmetros incluem:
> 
> - **Matriz intrínseca (K)**: representa os parâmetros internos da câmera, foco e centro óptico.
> - **dist**: Vetor de distorção, corrige imperfeições da lente considerando radial/tangencial.
> - **rvecs**: Vetores de rotação, orientações da câmera em relação ao tabuleiro em cada imagem.
> - **tvecs**: Vetores de translação, posições da câmera em relação ao tabuleiro em cada imagem.
> 
> Esses parâmetros são calculados usando a função `calibrateCamera` do OpenCV, que recebe os pontos de calibração e as imagens capturadas:

```python
# Calibrating left camera
retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(obj_pts,img_ptsL,imgL_gray.shape[::-1],None,None)

# Calibrating right camera
retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(obj_pts,img_ptsR,imgR_gray.shape[::-1],None,None)
```

> onde `mtxL` e `mtxR` são as matrizes intrínsecas para as câmeras esquerda e direita, respectivamente, `distL` e `distR` são os vetores de distorção, e `rvecsL`, `tvecsL` e `rvecsR`, `tvecsR` são os vetores de rotação e translação para cada câmera.

**3. Parâmetros extrínsecos**

> Os parâmetros extrínsecos descrevem a relação entre as duas câmeras, ou seja, como elas estão posicionadas e orientadas em relação uma à outra:
>
> - **R**: Matriz de rotação que alinha o sistema de coordenadas da câmera esquerda com o da câmera direita.
> - **T**: Vetor que descreve a translação da câmera esquerda em relação à direita.
> - **E**: Matriz essencial, combinação de R e T, usada para calcular a correspondência entre pontos nas duas imagens: $E = [T] \times R$
> - **F**: Matriz fundamental, que relaciona pares de pontos epipolares entre as imagens.
>
> Esses parâmetros são calculados usando a função `stereoCalibrate` do OpenCV, que recebe os pontos de calibração e as matrizes intrínsecas das câmeras:

```python
# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retS, new_mtxL, distL, new_mtxR, distR, Rot, Trns, Emat, Fmat = cv2.stereoCalibrate(obj_pts, img_ptsL, img_ptsR, new_mtxL, distL, new_mtxR, distR, imgL_gray.shape[::-1], criteria_stereo, flags)
```

> onde `Rot` é R, `Trns` é T, `Emat` é E e `Fmat` é F.

**4. Parâmetros de retificação e reprojeção**

> Os parâmetros de retificação e reprojeção são usados para alinhar as imagens capturadas e converter a disparidade em profundidade. Eles incluem:
>
> - **Matrizes de retificação (R1, R2)**: Rotacionam cada imagem para que os epípolos fiquem no infinito (linhas epipolares horizontais).
> - **Matrizes de projeção (P1, P2)**: Matriz de câmera “ajustada” após retificação, usada para reprojetar pixels.
> - **Matriz Q**: Matriz 4×4 que mapeia coordenadas de pixel e disparidade ($[x, y, d]$) em coordenadas de mundo $[X, Y, Z, 1]$: $[X, Y, Z, 1]^T = Q*[x, y, d, 1]^T$
> - **Regiões de interesse (ROI)**: Retângulos que definem as áreas válidas pós-retificação (para recorte).
>
> Esses parâmetros são calculados usando a função `stereoRectify` do OpenCV, que recebe as matrizes intrínsecas, os parâmetros extrínsecos e as dimensões da imagem:

```python
rect_l, rect_r, proj_mat_l, proj_mat_r, Q, roiL, roiR= cv2.stereoRectify(new_mtxL, distL, new_mtxR, distR, imgL_gray.shape[::-1], Rot, Trns, rectify_scale,(0,0))
```

> onde `rect_l` e `rect_r` são as matrizes de retificação para as câmeras esquerda e direita, respectivamente; `proj_mat_l` e `proj_mat_r` são as matrizes de projeção para as câmeras esquerda e direita, respectivamente; `Q` é a matriz Q; e `roiL` e `roiR` são as regiões de interesse (ROI) para as câmeras esquerda e direita, respectivamente.

> Em seguida, são gerados os mapas de remapeamento para corrigir distorção e aplicar retificação em tempo real. Esses mapas são calculados usando a função `initUndistortRectifyMap` do OpenCV:

```python
Left_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxL, distL, rect_l, proj_mat_l,
                                             imgL_gray.shape[::-1], cv2.CV_16SC2)

Right_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxR, distR, rect_r, proj_mat_r,
                                              imgR_gray.shape[::-1], cv2.CV_16SC2)
```

> Esses mapas contêm coordenadas de onde cada pixel de saída deve ser amostrado na imagem original.

### ANÁLISE E DISCUSSÃO DOS ESTUDOS REALIZADOS


### CONCLUSÕES




### REFERÊNCIAS CONSULTADAS E INDICADAS

- Introduction to Epipolar Geometry and Stereo Vision:
<https://learnopencv.com/introduction-to-epipolar-geometry-and-stereo-vision//>.
- Making A Low-Cost Stereo Camera Using OpenCV:
<https://learnopencv.com/making-a-low-cost-stereo-camera-using-opencv//>
