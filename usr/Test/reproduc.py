import tkinter as tk
from tkinter import filedialog
import vlc

# Crear una ventana tkinter
root = tk.Tk()
root.title("Reproductor de Video")

# Crear un reproductor VLC
instance = vlc.Instance()
player = instance.media_player_new()

# Función para abrir un archivo de video
def open_video():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos de Video", "*.mp4")])
    if file_path:
        media = instance.media_new(file_path)
        player.set_media(media)
        player.play()

# Función para pausar la reproducción
def pause():
    player.pause()

# Función para reanudar la reproducción
def play():
    player.play()

# Función para avanzar al siguiente
def next_video():
    # Aquí puedes agregar lógica para cargar y reproducir el siguiente video
    pass

# Botón para abrir un archivo de video
open_button = tk.Button(root, text="Abrir Video", command=open_video)
open_button.pack()

# Botón para pausar la reproducción
pause_button = tk.Button(root, text="Pausa", command=pause)
pause_button.pack()

# Botón para reanudar la reproducción
play_button = tk.Button(root, text="Reanudar", command=play)
play_button.pack()

# Botón para avanzar al siguiente video
next_button = tk.Button(root, text="Siguiente", command=next_video)
next_button.pack()

# Ventana principal
root.mainloop()
