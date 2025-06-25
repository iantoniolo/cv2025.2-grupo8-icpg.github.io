## Respostas do Laboratório 1 - Captura de Imagem e Vídeo
**ESZA019 – Visão Computacional**

**Membros do grupo:**

> - Ian Victor Toniolo Silva - 11202020351
> - Cesar Seiji Maruyama - 11127015
> - Pedro Henrique Cardoso Silva - 11202021250
> - Guilherme de Sousa Santos - 11201921175

**Data de realização dos experimentos:**
- 18/06/2025 (quarta-feira)

**Data de publicação do relatório:**
- 25/06/2025 (quarta-feira)

### INTRODUÇÃO
> O presente relatório tem como objetivo documentar as atividades realizadas no **Laboratório 1 - Captura de Imagem e Vídeo** da disciplina de Visão Computacional, abordando conceitos fundamentais relacionados à captura e manipulação de imagens e vídeos. Durante os experimentos, foram explorados aspectos práticos do uso da biblioteca OpenCV, como leitura, exibição, gravação e processamento básico de imagens e vídeos.

> Neste relatório, serão descritas as etapas realizadas para manipular imagens e vídeos, incluindo a leitura de arquivos, captura de frames de câmeras, ajustes de parâmetros como taxa de quadros (FPS) e operações básicas de processamento. Além disso, serão apresentados os resultados obtidos, como fotos e vídeos capturados durante os experimentos realizados também em laboratório, e discutidas as observações feitas ao longo do processo.

### PARTE 1: Processamento Básico nas Imagens e Vídeos

**(A) Leitura de imagem em arquivo**
> A janela não mostra a imagem colorida pois o segundo parâmetro da função `cv.imread()` foi atribuído o valor `0`, que representa ausência de cor no modo de leitura. Caso a atribuição seja `cv.IMREAD_COLOR_BGR` a imagem será convertida para os canais RBG (Red-Blue-Green) e a saída será uma imagem colorida.
>
> Para corrigir isso, basta alterar a linha de leitura da imagem para:

```python
img = cv.imread('messi5.jpg',cv.IMREAD_COLOR_BGR)
```
> Dessa forma, a imagem será lida corretamente com as cores e apresentada na janela da seguinte forma:

![alt text](messi-com-cores.png "Title")

**(B) Leitura de vídeo em arquivo**
> A velocidade de exibição do vídeo, ou seja, a velocidade com que os frames são exibidos na tela depende do tempo de espera entre a exibição de cada frame, controlado pela linha `time.sleep(1/25.0)` (simula um atraso de 40ms).

> Para aumentar a velocidade, basta diminuir o tempo de espera através de um acréscimo no valor do denomidador. Por exemplo, se quisermos aumentar para 50fps, basta fazer a seguinte alteração:

```python
time.sleep(1/50.0)
```

> Para reduzir a velocidade, basta aumentar o tempo de espera. Por exemplo, se quisermos diminuir para 10fps, basta fazer a seguinte alteração:

```python
time.sleep(1/10.0)
```

**(C) Leitura de imagem de câmera**
> Para salvar o frame ao pressionar a tecla 'x', basta adicionar o seguinte comando:

```python
if key == ord('x'):
    cv.imwrite('foto1.png', frame)
    print("Frame saved as 'foto1.png'")
```

**(D) Gravação de vídeo da câmera**
> Para que a saída do vídeo esteja "normal", ou seja, sem a inversão vertical e com uma velocidade adequada, basta remover o comando `cv.flip(frame, 0)` que inverte a imagem verticalmente e ajustar o valor da variável `fps` para um valor mais alto, como `60.0`, que é uma taxa de quadros comum para vídeos. Assim, o código para exibir e salvar o vídeo ficará assim:

```python
import numpy as np
import cv2 as cv

cap = cv.VideoCapture(2)

# Get current width of frame
width = cap.get(cv.CAP_PROP_FRAME_WIDTH)   # float
# Get current height of frame
height = cap.get(cv.CAP_PROP_FRAME_HEIGHT) # float
# Define Video Frame Rate in fps
fps = 60.0

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')
out = cv.VideoWriter('saida.avi', fourcc, fps, (int(width),int(height)) )

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # write the flipped frame
    out.write(frame)
    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

# Release everything if job is finished
cap.release()
out.release()
cv.destroyAllWindows()
```

**Responda: se for necessário alterar a imagem, ou seja realizando alguma operação de procesamento nela, em que ponto dos quatro programas estudados isso deve ser realizado?**
> As operações de processamento de imagem devem ser realizadas após a leitura da imagem ou do frame do vídeo, mas antes de exibi-los ou salvá-los.

### PARTE 2: Obtenção de Fotos e Vídeos

**(A) Obtenção de foto da equipe**

**(B) Foto Avatar da equipe**

**(C) Vídeos com pessoas e com objeto**

> O seguinte vídeo foi gravado com uma pessoa realizando movimentos rápidos com as mãos:

<video width="320" height="240" controls>
  <source src="./video-pessoa-rapido.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

> O seguinte vídeo foi gravado com uma pessoa realizando movimentos lentos com as mãos:

<video width="320" height="240" controls>
  <source src="./video_pessoa_lento.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>

> O seguinte vídeo foi gravado com um objeto (um livro) realizando movimentos rápidos:


> O seguinte vídeo foi gravado com um objeto (um livro) realizando movimentos lentos:

### ANÁLISE E CONCLUSÃO

### REFERÊNCIAS
- OpenCV Documentation: https://docs.opencv.org/
- OpenCV Python Tutorials: https://opencv-python-tutroals.readthedocs.io