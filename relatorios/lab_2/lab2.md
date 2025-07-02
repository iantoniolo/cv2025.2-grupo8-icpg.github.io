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

##### (A) O procedimento de calibração de câmera com imagens fornecidas de exemplo

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
