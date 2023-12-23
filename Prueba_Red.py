import cv2
import numpy as np
from tensorflow.keras.models import load_model
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

def prepare_image(file_path):
    img_size = 150  # El mismo tamaño que usaste para el entrenamiento
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    img_resized = cv2.resize(img, (img_size, img_size))
    img_resized = np.array(img_resized) / 255.0  # Normalizar
    img_resized = img_resized.reshape(1, img_size, img_size, 1)  # Cambiar forma para el modelo
    return img, img_resized

# Cargar el modelo
modelo = load_model('modelo_neumonia_mejorado2.tf')

# Iniciar interfaz gráfica para seleccionar imagen
root = tk.Tk()
root.withdraw()  # No queremos una ventana completa de Tk, solo el dialogo
file_path = filedialog.askopenfilename()  # Abrir dialogo para seleccionar archivo

if file_path:
    original_image, test_image = prepare_image(file_path)
    prediction = modelo.predict(test_image)
    predicted_class = np.argmax(prediction, axis=1)

    plt.imshow(original_image, cmap='gray')
    plt.axis('off')  # No mostrar ejes

    if predicted_class[0] == 0:
        plt.title("Clasificación: Normal")
    else:
        plt.title("Clasificación: Neumonía")

    plt.show()
else:
    print("No se seleccionó ninguna imagen.")
