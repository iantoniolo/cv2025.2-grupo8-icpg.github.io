## Relatório Laboratório 3 – Camera Estéreo

**ESZA019 – Visão Computacional**

**Membros do grupo:**

> - Ian Victor Toniolo Silva - 11202020351
> - Cesar Seiji Maruyama - 11127015
> - Pedro Henrique Cardoso Silva - 11202021250
> - Guilherme de Sousa Santos - 11201921175

**Data de realização dos experimentos:**
- 16/07/2025 (quarta-feira)

**Data de publicação do relatório:**
- 21/07/2025 (segunda-feira)

### INTRODUÇÃO


### PROCEDIMENTOS EXPERIMENTAIS

#### (A) Obtenção dos códigos do exemplo da câmera estéreo com OpenCV

Para executar os procedimentos, baixe o seguinte código de exemplo: https://github.com/spmallick/learnopencv/tree/master/stereo-camera

#### (B) Execute o exemplo com as imagens fornecidas

A calibração de câmeras consiste em estimar os parâmetros intrínsecos e extrínsecos de uma ou mais câmeras com base em imagens de um padrão conhecido, como um tabuleiro de xadrez. A calibração é essencial para corrigir distorções nas imagens capturadas pela câmera, além de ajudar a determinar as relações espaciais entre as câmeras em um sistema estéreo como o utilizado em laboratório.

Parâmetros necessários para a calibração de câmeras:

- Parâmetros intrínsecos:

Matriz da câmera (matriz intrínseca): Contém informações sobre a lente da câmera, como a distância focal (f_x, f_y) e o ponto principal (normalmente o centro da imagem, c_x, c_y).

CameraMatrix=[fx0cx0fycy001]

CameraMatrix=​fx​00​0fy​0​cx​cy​1​
            
Coeficientes de distorção: Corrigem distorções causadas pela lente da câmera (como distorções radiais e tangenciais). Os coeficientes comuns são:

k1,k2,k3k1​,k2​,k3​ (distorção radial)

p1,p2p1​,p2​ (distorção tangencial)

Parâmetros extrínsecos:

Matriz de rotação (R): Descreve a orientação relativa entre a câmera e o sistema de coordenadas do mundo.

Vetor de translação (T): Descreve a posição relativa da câmera em relação ao sistema de coordenadas do mundo.

Para um sistema estéreo, os parâmetros adicionais incluem:

Matriz de rotação entre as câmeras (R): Define a rotação relativa entre a câmera esquerda e a direita.

Vetor de translação entre as câmeras (T): Define a distância e direção entre as duas câmeras.

Esses parâmetros permitem que você reconstrua a cena 3D a partir de imagens 2D capturadas por cada câmera.

#### (C) Execute a Calibração da sua câmera estéreo (construída com as webcams) pela
captura de suas próprias imagens de calibração e imagens de teste

#### (D) Realize a gravação de um video 3D com sua câmera estéreo

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
