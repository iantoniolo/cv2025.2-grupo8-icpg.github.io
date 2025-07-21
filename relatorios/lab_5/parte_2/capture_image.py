import cv2

# Abrir a webcam (índice 0 é o dispositivo de webcam padrão)
cap = cv2.VideoCapture(0)

# Verificar se a câmera foi aberta corretamente
if not cap.isOpened():
    print("Erro ao abrir a webcam.")
    exit()

# Exibir a captura da webcam
print("Pressione 's' para tirar uma foto ou 'q' para sair.")

while True:
    # Captura frame por frame
    ret, frame = cap.read()
    
    # Verificar se a captura foi bem-sucedida
    if not ret:
        print("Erro ao capturar a imagem.")
        break
    
    # Exibir a imagem capturada na janela
    cv2.imshow('Pressione "s" para salvar ou "q" para sair', frame)

    # Aguardar por tecla
    key = cv2.waitKey(1) & 0xFF
    
    # Se pressionar 's', salva a imagem
    if key == ord('s'):
        cv2.imwrite('box_in_scene.png', frame)  # Salva a imagem com o nome desejado
        print("Imagem salva como 'box_in_scene.png'")
        break
    
    # Se pressionar 'q', sai
    elif key == ord('q'):
        print("Saindo...")
        break

# Libera a captura e fecha as janelas
cap.release()
cv2.destroyAllWindows()
