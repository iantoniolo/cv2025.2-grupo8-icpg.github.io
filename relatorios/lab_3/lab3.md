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

Este relatório detalha os experimentos realizados no Laboratório 3 (Câmera Estéreo), focado no estudo e aplicação da estereoscopia em visão computacional. A estereoscopia é a técnica que permite a percepção de profundidade a partir de duas imagens capturadas de pontos de vista ligeiramente diferentes, de forma análoga à visão humana. O objetivo deste trabalho foi construir e calibrar um sistema de câmera estéreo de baixo custo, utilizando duas webcams providas em laboratório, para compreender na prática os conceitos de geometria epipolar e reconstrução 3D. Ao longo deste documento, serão descritos os procedimentos para a montagem do aparato experimental, a calibração individual e conjunta das câmeras para obtenção dos parâmetros intrínsecos e extrínsecos, e a geração de imagens. A análise dos resultados demonstrará a viabilidade de se criar um sistema de percepção de profundidade e as implicações dos parâmetros de calibração na qualidade da reconstrução tridimensional.

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

##### (A) Obtenção dos códigos do exemplo da câmera estéreo com OpenCV

Para executar os procedimentos, baixe o seguinte código de exemplo: https://github.com/spmallick/learnopencv/tree/master/stereo-camera

##### (B) Execute o exemplo com as imagens fornecidas:

A calibração de câmeras consiste em estimar os parâmetros intrínsecos e extrínsecos de uma ou mais câmeras com base em imagens de um padrão conhecido, como um tabuleiro de xadrez. A calibração é essencial para corrigir distorções nas imagens capturadas pela câmera, além de ajudar a determinar as relações espaciais entre as câmeras em um sistema estéreo como o utilizado em laboratório.

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

##### (C) Execute a Calibração da sua câmera estéreo (construída com as webcams) pela captura de suas próprias imagens de calibração e imagens de teste

> Para capturar as imagens de calibração, utilizamos um padrão de tabuleiro de xadrez (9,7) disponibilizado no laboratório. As imagens foram capturadas com as duas câmeras simultaneamente, garantindo que ambas estivessem alinhadas e fixas.
>
> Primeiro, altere os índices das câmeras no código para corresponder às webcams utilizadas. Em nosso caso, as câmeras foram identificadas como `CamL_id = 2` e `CamR_id = 4`. Certifique-se de que as câmeras estejam conectadas e reconhecidas pelo sistema:

```python
# Check for left and right camera IDs
CamL_id = 2
CamR_id = 4
```

> Configure também o caminho para salvar as imagens capturadas:

```python
output_path = "./data-lab/"
```

> Em seguida, execute o script `capture_images.py` para capturar entre 10 e 15 imagens de calibração. O script irá abrir uma janela de visualização onde você deve posicionar o padrão de tabuleiro de xadrez em frente às câmeras. O script realizará a captura automaticamente a cada 10 segundos. Certifique-se de que o fundo esteja bem iluminado e visível para ambas as câmeras.

```shell
python3 capture_images.py
```

> Após capturar as imagens, verifique se as imagens foram salvas corretamente no diretório especificado. As imagens das câmeras esquerda e direita devem estar nas respectivas pastas `stereoL` e `stereoR` dentro do diretório `data-lab`. As imagens devem ser nomeadas de forma numérica (por exemplo, `img1.jpg`, `img2.jpg`, etc.).
>
> Agora, acesse o script `calibrate.py` para alterar o valor de algumas variáveis. Primeiro, altere o caminho para as imagens capturadas:

```python
# Set the path to the images captured by the left and right cameras
pathL = "./data-lab/stereoL/"
pathR = "./data-lab/stereoR/"
```

> Em seguida, ajuste os parâmetros de calibração, como o tamanho do tabuleiro de xadrez e o número de imagens a serem processadas:

```python
objp = np.zeros((8*6,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)
```

```python
retR, cornersR =  cv2.findChessboardCorners(outputR,(8,6),None)
retL, cornersL = cv2.findChessboardCorners(outputL,(8,6),None)
```

> Ajuste também o caminho para salvar os resultados da calibração:

```python
cv_file = cv2.FileStorage("./data-lab/params_py.xml", cv2.FILE_STORAGE_WRITE)
```

> Execute o script `calibrate.py` para realizar a calibração das câmeras estéreo. O script irá processar as imagens capturadas, calcular os parâmetros intrínsecos e extrínsecos, e salvar os resultados no arquivo XML indicado na linha acima.

```shell
python3 calibrate.py
```

**Responda: liste todos os parâmetros e valores obtidos para sua câmera estéreo, colocando-os nas formas de matrizes e vetores. Quais destes parâmetros forma salvos no arquivo de parâmetros de calibração (xml)?**

> Os parâmetros obtidos para a câmera estéreo foram os seguintes:

> **Parâmetros intrínsecos (câmera esquerda)**

**Matriz intrínseca (K)**:

```
[[677.73412452   0.         307.55974464]
 [  0.         679.11055189 215.06111841]
 [  0.           0.           1.        ]]
```

**dist**:

```
[[ 9.44064482e-02 -1.02738043e+00 -2.87071648e-03 -8.87143372e-04 4.25419033e+00]]
```

**rvecs**:

```
(array([[-0.18726085],
       [-0.1471088 ],
       [ 0.07278578]]), array([[-0.08479358],
       [-0.21444249],
       [ 0.06833422]]), array([[-0.1161428 ],
       [-0.19247522],
       [ 0.07515873]]), array([[-0.10871448],
       [-0.20476947],
       [ 0.07130746]]), array([[-0.12125288],
       [-0.22100292],
       [ 0.07579088]]), array([[-0.15515976],
       [-0.21326652],
       [ 0.05983969]]), array([[-0.16168664],
       [-0.22186651],
       [ 0.06242239]]), array([[-0.18518884],
       [-0.10420233],
       [ 0.05875823]]), array([[-0.27565159],
       [-0.01013508],
       [-0.06055519]]), array([[-4.18249557e-01],
       [-2.67449122e-01],
       [-2.57701520e-04]]), array([[-0.18515866],
       [-0.08204098],
       [-0.00902972]]), array([[-0.17829982],
       [-0.19904146],
       [ 0.12443069]]), array([[-0.11727435],
       [-0.21784396],
       [-0.07667582]]), array([[-0.15950268],
       [-0.24466782],
       [-0.03354782]]))
```

**tvecs**:

```
(array([[-4.00258862],
       [-0.98543208],
       [20.5407316 ]]), array([[-3.65888606],
       [-1.4118987 ],
       [15.38243461]]), array([[-3.96383953],
       [-1.45569517],
       [15.70983332]]), array([[-3.98282811],
       [-1.37375808],
       [15.76913313]]), array([[-3.97610417],
       [-1.35312241],
       [16.07602975]]), array([[-4.51885247],
       [-1.48594896],
       [16.47496932]]), array([[-4.3727964 ],
       [-1.55823785],
       [16.70674578]]), array([[-3.14332462],
       [-2.0476241 ],
       [18.26171255]]), array([[-2.90593551],
       [-0.97678094],
       [20.56173821]]), array([[-3.48937015],
       [-1.67685431],
       [16.85178941]]), array([[-3.27081821],
       [-2.30339502],
       [17.21697277]]), array([[-3.39743476],
       [-1.86045594],
       [17.61692777]]), array([[-4.28046869],
       [-0.71486803],
       [19.42886085]]), array([[-2.75866594],
       [-1.3680894 ],
       [19.76986144]]))
```

> **Parâmetros intrínsecos (câmera direita)**

**Matriz intrínseca (K) - direita**:

```
[[662.20625692   0.         303.89626902]
 [  0.         663.65175243 242.31022247]
 [  0.           0.           1.        ]]
```

**dist - direita**:

```
[[-1.26556519e-02  8.25228739e-01 -2.11672103e-03 -3.87764451e-03 -5.16015391e+00]]
```

**rvecs**:

```
(array([[-0.11775436],
       [-0.02568732],
       [ 0.07096546]]), array([[-0.01975621],
       [-0.09092623],
       [ 0.05700549]]), array([[-0.04723013],
       [-0.07010609],
       [ 0.06659752]]), array([[-0.0425551 ],
       [-0.08123578],
       [ 0.06217378]]), array([[-0.05498146],
       [-0.09493236],
       [ 0.06663226]]), array([[-0.08924682],
       [-0.08957561],
       [ 0.05322777]]), array([[-0.09241702],
       [-0.0974973 ],
       [ 0.05632886]]), array([[-0.11632127],
       [ 0.01772641],
       [ 0.0585464 ]]), array([[-0.20703201],
       [ 0.11334338],
       [-0.05178392]]), array([[-0.34730923],
       [-0.13988738],
       [ 0.00824827]]), array([[-0.11239395],
       [ 0.04454306],
       [-0.00789479]]), array([[-0.10436183],
       [-0.07620069],
       [ 0.11896787]]), array([[-0.06395512],
       [-0.08928769],
       [-0.08528989]]), array([[-0.09707344],
       [-0.11571809],
       [-0.04067226]]))
```

**tvecs**:

```
(array([[-3.46781001],
       [-2.49181903],
       [20.26492569]]), array([[-3.77577532],
       [-2.54816938],
       [15.21901132]]), array([[-4.0320972 ],
       [-2.61317282],
       [15.55499563]]), array([[-4.03357237],
       [-2.53775742],
       [15.62615583]]), array([[-3.98475441],
       [-2.53503718],
       [15.92701444]]), array([[-4.45893279],
       [-2.69723497],
       [16.36256548]]), array([[-4.27958184],
       [-2.78425209],
       [16.55234704]]), array([[-2.85571823],
       [-3.38638036],
       [17.8937489 ]]), array([[-2.32765742],
       [-2.50073183],
       [20.16242011]]), array([[-3.36467159],
       [-2.91296352],
       [16.58793849]]), array([[-3.10783497],
       [-3.5957032 ],
       [16.86303783]]), array([[-3.17202942],
       [-3.15277506],
       [17.297533  ]]), array([[-3.78496225],
       [-2.14030538],
       [19.24359366]]), array([[-2.23864618],
       [-2.8190647 ],
       [19.33709621]]))
```

> **Parâmetros extrínsecos**

**R**:

```
[[ 0.96600108  0.03046948  0.2567363 ]
 [-0.02231146  0.99915113 -0.03462975]
 [-0.25757352  0.02772421  0.96586089]]
```

**T**:

```
[[-3.24048731]
 [-0.79568461]
 [-3.97249102]]
```

**E**:

```
[[ 0.11631519  3.94705917 -0.90608699]
 [-4.67209432 -0.03119977  2.1099773 ]
 [ 0.8409322  -3.21349247  0.31649837]]
```

**F**:

```
[[ 1.18900200e-06  4.07439858e-05 -1.54862954e-02]
 [-4.14411985e-05 -2.79457547e-07  2.57228714e-02]
 [ 1.40272153e-02 -2.67164065e-02  1.00000000e+00]]
```

> **Parâmetros de retificação e reprojeção**

**Matrizes de retificação (R1, R2)**:

```
Rectification transformation (left): [[ 0.40273389  0.19350308  0.89462952]
 [-0.17179171  0.97600884 -0.13376976]
 [-0.89905118 -0.09981632  0.42631406]]
```

```
Rectification transformation (right): [[ 0.62462118  0.15337244  0.76571879]
 [-0.17055605  0.98364567 -0.05789491]
 [-0.76207546 -0.09443558  0.64056452]]
```

**Matrizes de projeção (P1, P2)**:

```
Projection matrix (left): [[ 6.21037622e+02  0.00000000e+00 -5.96954103e+03  0.00000000e+00]
 [ 0.00000000e+00  6.21037622e+02  7.66792057e+02  0.00000000e+00]
 [ 0.00000000e+00  0.00000000e+00  1.00000000e+00  0.00000000e+00]]
```

```
Projection matrix (right): [[ 6.21037622e+02  0.00000000e+00 -5.96954103e+03 -3.22189608e+03]
 [ 0.00000000e+00  6.21037622e+02  7.66792057e+02  0.00000000e+00]
 [ 0.00000000e+00  0.00000000e+00  1.00000000e+00  0.00000000e+00]]
```

**Matriz Q**:

```
Q: [[ 1.00000000e+00  0.00000000e+00  0.00000000e+00  5.96954103e+03]
 [ 0.00000000e+00  1.00000000e+00  0.00000000e+00 -7.66792057e+02]
 [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  6.21037622e+02]
 [ 0.00000000e+00  0.00000000e+00  1.92755324e-01 -0.00000000e+00]]
```

**Regiões de interesse (ROI)**

```
ROI (left): (0, 0, 0, 0)
ROI (right): (0, 0, 0, 0)
```

**Mapa de remapeamento**

```
Left Stereo Map: (array([[[547, 255],
        [547, 255],
        [547, 255],
        ...,
        [554, 265],
        [554, 265],
        [554, 265]],

       [[547, 255],
        [547, 255],
        [547, 255],
        ...,
        [554, 265],
        [554, 265],
        [554, 265]],

       [[547, 255],
        [547, 255],
        [547, 255],
        ...,
        [554, 265],
        [554, 265],
        [554, 265]],

       ...,
```

```
Right Stereo Map: (array([[[480, 252],
        [480, 252],
        [480, 252],
        ...,
        [469, 257],
        [469, 257],
        [468, 257]],

       [[480, 252],
        [480, 252],
        [480, 252],
        ...,
        [469, 257],
        [469, 257],
        [468, 257]],

       [[480, 252],
        [480, 252],
        [480, 252],
        ...,
        [469, 257],
        [469, 257],
        [469, 257]],

       ...,
```

> Os parâmetros salvos no arquivo XML de calibração foram:

```python
Left_Stereo_Map[0]
Left_Stereo_Map[1]
Right_Stereo_Map[0]
Right_Stereo_Map[1]
```

#### (D) Realize a gravação de um video 3D com sua câmera estéreo

Este guia explica como capturar vídeos em tempo real com câmeras estéreo, corrigir distorções nas imagens, combinar as imagens para criar um efeito 3D e gravar o resultado em um arquivo MP4.

##### 1. **Configuração do Ambiente**

##### 1.1. Instalação das Dependências

Certifique-se de ter o OpenCV e o Numpy instalados. Se não os tiver, instale-os com o seguinte comando:

```bash
pip install opencv-python opencv-python-headless numpy
```

##### 2.1. Abrindo as Câmeras

As câmeras são abertas utilizando os índices correspondentes, que podem ser números inteiros (como 0 para a câmera esquerda e 1 para a câmera direita, verifique os IDs das suas câmeras).

```python
# IDs das câmeras (substitua pelos índices corretos das suas câmeras)
CamL_id = 0  # Câmera esquerda
CamR_id = 1  # Câmera direita

# Abrir as câmeras para captura em tempo real
CamL = cv2.VideoCapture(CamL_id)
CamR = cv2.VideoCapture(CamR_id)

# Verificar se as câmeras foram abertas corretamente
if not CamL.isOpened() or not CamR.isOpened():
    print("Erro ao abrir as câmeras.")
    exit()
```

##### 3.1. Configuração do Arquivo de Saída

O arquivo de saída é configurado para salvar o vídeo 3D com o codec H264, em formato MP4. A resolução do vídeo de saída é definida pela resolução das câmeras.

```python
# Tamanho do quadro das câmeras
frame_width = int(CamL.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(CamL.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Definir codec e arquivo de saída
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec H264
out = cv2.VideoWriter('./video3d_output.mp4', fourcc, 30.0, (frame_width, frame_height))
```

Este código configura o arquivo de saída onde o vídeo 3D será salvo.

##### 5. Execução do Arquivo

Para rodar o script:

    Salve o código em um arquivo Python, como capture_3d_video.py.

    Execute o script no terminal:

```python
python capture_3d_video.py
```

O script abrirá as câmeras em tempo real, aplicará a correção de distorção, criará o efeito 3D, exibirá o vídeo 3D e gravará o resultado no arquivo video3d_output.mp4.

##### Resultado

Você deve obter um resultado parecido com isso:

<video width="700" height="700" controls>
    <source src="stereo-camera/3d_output_video.avi" type="video/mp4">
    Your browser does not support the video tag.
</video>

### ANÁLISE E DISCUSSÃO DOS ESTUDOS REALIZADOS

A montagem e calibração do sistema de câmera estéreo permitiram uma análise aprofundada da relação entre a teoria da geometria epipolar e sua aplicação prática. O processo de calibração, realizado com o padrão de xadrez, foi a etapa mais crítica, pois a precisão dos parâmetros intrínsecos (matriz da câmera e coeficientes de distorção) e, principalmente, dos extrínsecos (rotação `R` e translação `T` entre as câmeras) define a qualidade da reconstrução 3D. O vetor de translação `T`, em particular, estabelece a linha de base (baseline) do sistema, influenciando diretamente a sensibilidade da medição de profundidade: uma base maior tende a melhorar a acurácia para objetos distantes, enquanto uma base menor é mais adequada para cenas próximas.

Após a calibração, a etapa de retificação alinhou horizontalmente as linhas epipolares das imagens esquerda e direita. Esse processo é fundamental, pois simplifica o problema de correspondência de pontos (stereo matching) a uma busca unidimensional ao longo da mesma linha de pixels. A eficácia dessa retificação foi visível na geração do mapa de disparidade. No mapa gerado, observou-se que objetos mais próximos da câmera apresentavam valores de disparidade maiores (cores mais claras), enquanto objetos distantes tinham disparidades menores (cores mais escuras), o que é consistente com o princípio da estereoscopia.

No entanto, também foram identificados alguns desafios. Regiões com pouca textura, superfícies reflexivas ou áreas que são visíveis por apenas uma das câmeras resultaram em "buracos" ou ruídos no mapa de disparidade, onde o algoritmo de correspondência falhou em encontrar um par válido. A geração da imagem anaglífica, que requer o uso de óculos 3D, proporcionou uma avaliação qualitativa e intuitiva da percepção de profundidade, confirmando que o sistema foi capaz de codificar a informação tridimensional de forma eficaz, apesar das limitações observadas no mapa de disparidade.

### CONCLUSÕES

Este laboratório demonstrou com sucesso a viabilidade de construir um sistema de visão estéreo funcional e de baixo custo utilizando componentes acessíveis como webcams. Os objetivos propostos foram alcançados, consolidando o entendimento prático dos conceitos de geometria epipolar, calibração de múltiplas câmeras e reconstrução 3D.

### REFERÊNCIAS CONSULTADAS E INDICADAS

- [1] Making A Low-Cost Stereo Camera Using OpenCV:
<https://learnopencv.com/making-a-low-cost-stereo-camera-using-opencv/>
Código: <https://github.com/spmallick/learnopencv/tree/master/stereo-camera>
- [2] Introduction to Epipolar Geometry and Stereo Vision:
<https://learnopencv.com/introduction-to-epipolar-geometry-and-stereo-vision/>
Código:
<https://github.com/spmallick/learnopencv/tree/master/EpipolarGeometryAndSter
eoVision>
- [3] Understanding Lens Distortion:
<https://learnopencv.com/understanding-lens-distortion/>
Código:
<https://github.com/spmallick/learnopencv/tree/master/UnderstandingLensDistort
ion>
- [4] C. Loop and Z. Zhang. Computing Rectifying Homographies for Stereo Vision.
IEEE Conf. Computer Vision and Pattern Recognition, 1999.
- [5] Geometry of Image Formation:
<https://learnopencv.com/geometry-of-image-formation/>
