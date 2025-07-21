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

> Execute o script `calibrate.py` para realizar a calibração das câmeras estéreo. O script irá processar as imagens capturadas, calcular os parâmetros intrínsecos e extrínsecos, e salvar os resultados em um arquivo XML.

```shell
python3 calibrate.py
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

<video width="320" height="320" controls>
    <source src="./stereo-camera/3d_output_video.mp4" type="video/mp4">
</video>

### ANÁLISE E DISCUSSÃO DOS ESTUDOS REALIZADOS

### CONCLUSÕES

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
