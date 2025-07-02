## Relatório Laboratório 2 – Calibração de Cameras

**ESZA019 – Visão Computacional**

**Membros do grupo:**

> - Ian Victor Toniolo Silva - 11202020351
> - Cesar Seiji Maruyama - 11127015
> - Pedro Henrique Cardoso Silva - 11202021250
> - Guilherme de Sousa Santos - 11201921175

**Data de realização dos experimentos:**
- 25/06/2025 (quarta-feira)

**Data de publicação do relatório:**
- 30/06/2025 (segunda-feira)

### INTRODUÇÃO


---

### PROCEDIMENTOS EXPERIMENTAIS

#### PARTE 1: Estudo da teoria sobre parâmetros da geometria de câmeras. 

A formação de imagens em visão computacional baseia-se no modelo de câmera pinhole, no qual o mundo tridimensional é projetado em um plano bidimensional, como o sensor de uma câmera. De forma simplificada, nesse modelo, cada ponto do espaço é imaginado passando por um “orifício” até chegar ao plano da imagem, criando uma relação direta entre a posição 3D e sua projeção 2D. Isso permite, por exemplo, entender como a distância do objeto à câmera e as características óticas e como a distância focal influenciam o tamanho e também o posicionamento dos elementos capturados na imagem.

Para usar a câmera como um instrumento de medição confiável, é necessário determinar seus parâmetros internos (tipo a distância focal efetiva e o centro óptico) e corrigir as imperfeições das lentes. A calibração de câmera consiste em capturar imagens de um padrão conhecido, comparar as projeções observadas com as esperadas e, a partir disso, ajustar os parâmetros para que a correspondência seja precisa. Além disso, deve-se levar em conta a distorção radial, que faz com que linhas retas pareçam curvar-se nas bordas da imagem, e a distorção tangencial, que surge de pequenos desalinhamentos no conjunto ótico. Uma vez calibrada, a câmera pode gerar imagens “retificadas”, nas quais os defeitos de lente são minimizados consideravelmente e assim é melhora  a qualidade de aplicações como reconstrução 3D, medição de distâncias e também navegação robótica.

#### PARTE 2: Executar um exemplo de calibração de câmeras.

##### (A) O procedimento de calibração de câmera com imagens fornecidas de exemplo.

##### Parâmetros da Calibração da Câmera

**Matriz Intrínseca (K)**

```
K =
[[536.07345296   0.         342.37047282]
 [  0.         536.01636332 235.53687702]
 [  0.           0.           1.        ]]
```

**Vetor de Distorção (dist)**

```
dist =
[[-0.26509044 -0.04674186  0.00183301 -0.00031469  0.25231154]]
```

**Vetores de Rotação**

```
rvecs = [
 [ 0.48287277], [-0.17037078], [-1.40740327],
 [-0.35339067], [ 0.24071863], [ 0.20970027],
 [ 0.19721096], [-0.42009963], [-0.1949708 ],
 [-0.08398729], [ 0.34802798], [-1.54244125],
 [-0.34698232], [-0.06738512], [-1.20088998],
 [-0.22584613], [ 1.0155115 ], [-2.79470623],
 [-0.37463355], [ 0.06982818], [-0.01937111],
 [ 0.06525918], [ 0.44701842], [ 0.10800013],
 [-0.10141629], [ 0.32034812], [ 0.3147293 ],
 [ 0.49542336], [ 0.11948808], [-0.29675958],
 [-0.4735952 ], [ 0.08970834], [-0.22605981],
 [ 0.05280128], [-0.60171832], [-0.18453815],
 [-0.27527313], [ 0.10123349], [-1.56296568]
]
```

**Vetores de Translação (tvecs)**

```
tvecs = [
 [-3.50264637], [ 1.61595404], [11.97222152],
 [-1.59004095], [-4.31771235], [14.01040668],
 [-2.67642941], [-3.18945602], [10.58262241],
 [-2.96218417], [ 0.57158932], [16.83013775],
 [-3.427436  ], [ 0.4873819 ], [11.56153507],
 [ 2.53399419], [ 4.31999128], [13.71919122],
 [-2.95848731], [-3.94417974], [13.21423743],
 [ 2.20741839], [-3.21446613], [15.60125394],
 [-3.72585434], [-4.3108485 ], [17.20439703],
 [-3.40557514], [-2.41042315], [12.58706805],
 [-2.51791826], [-3.43069105], [12.85702135],
 [-2.16838794], [-3.50011196], [10.73694991],
 [-3.99388098], [ 2.27704343], [12.68878108]
]
```

Configura algumas das imagens utilizadas:

<img src="./arquivos/samples/left01.jpg" width=420>

<br>

<img src="./arquivos/samples/left02.jpg" width=420>

**Significado dos Parâmetros**

- **K**: Matriz intrínseca, representa os parâmetros internos da câmera, foco e centro óptico.
- **dist**: Vetor de distorção, corrige imperfeições da lente considerando radial/tangencial.
- **rvecs**: Vetores de rotação, orientações da câmera em relação ao tabuleiro em cada imagem.
- **tvecs**: Vetores de translação, posições da câmera em relação ao tabuleiro em cada imagem.

##### (B) Calibração da sua webcam com a captura de suas próprias imagens de calibração

##### (C) Realize a calibração de uma outra câmera pessoal:

### ANÁLISE E DISCUSSÃO DOS ESTUDOS REALIZADOS

### CONCLUSÕES

### REFERÊNCIAS CONSULTADAS E INDICADAS

- A geometria da formação de imagens:
<https://learnopencv.com/geometry-of-image-formation/>.
- Teoria da Calibração de Camera com OpenCV:
<https://learnopencv.com/camera-calibration-using-opencv/>
- Atenção na parte de Distorção Radial da Lentes:
<https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html>.
