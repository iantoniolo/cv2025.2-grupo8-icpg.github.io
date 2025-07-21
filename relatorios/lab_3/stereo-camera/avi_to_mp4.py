from moviepy.editor import VideoFileClip

# Caminho para o arquivo .avi
avi_file = "saida.avi"

# Caminho para salvar o arquivo .mp4
mp4_file = "output_video.mp4"

# Carregar o vídeo .avi
video = VideoFileClip(avi_file)

# Escrever o arquivo de saída em formato MP4
video.write_videofile(mp4_file, codec="libx264")

print("Conversão concluída!")
