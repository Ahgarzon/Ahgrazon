import os
import cv2
import numpy as np
from tensorflow.keras.utils import to_categorical #se utiliza para convertir vectores de etiquetas enteras en una representación binaria.
from sklearn.model_selection import train_test_split # se usa para dividir arrays o matrices en subconjuntos aleatorios de entrenamiento y prueba.
from tensorflow.keras.models import Sequential # Keras, que es un modelo lineal de apilamiento de capas.
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout  #Importa varios tipos de capas de Keras necesarios para construir la CNN.

# Directorios de datos
base_dir = r'D:\Semestre 8\VISION DE MAQUINA\Trabajo final\archive\chest_xray'
train_dir = os.path.join(base_dir, 'train')
test_dir = os.path.join(base_dir, 'test')

# Parámetros
img_size = 150  # Redimensionar imágenes

def load_images_from_folder(folder): #Define una función para cargar imágenes desde un directorio.
    images = [] #Inicializa una lista vacía para almacenar imágenes.
    labels = [] # Inicializa una lista vacía para almacenar etiquetas.
    for subdir, dirs, files in os.walk(folder): #Recorre todos los subdirectorios y archivos en el directorio dado.
        for file in files: # Itera sobre cada archivo en el directorio.
            img_path = os.path.join(subdir, file) #Obtiene la ruta completa de la imagen.
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE) #Lee la imagen en escala de grises.
            if img is not None: #Verifica si la imagen se ha leído correctamente.
                img = cv2.resize(img, (img_size, img_size)) #Redimensiona la imagen al tamaño especificado.
                images.append(img) #Añade la imagen a la lista de imágenes.
                label = 1 if 'PNEUMONIA' in subdir else 0 #Asigna una etiqueta basada en si la palabra 'PNEUMONIA' está en el nombre del subdirectorio.
                labels.append(label) #Añade la etiqueta a la lista de etiquetas.
    return images, labels #Retorna las imágenes y las etiquetas.

# Cargar imágenes
train_images, train_labels = load_images_from_folder(train_dir) #Carga imágenes y etiquetas de entrenamiento.
test_images, test_labels = load_images_from_folder(test_dir) #Carga imágenes y etiquetas de prueba.

# Convertir a arrays de numpy y normalizar
train_images = np.array(train_images) / 255.0 #Convierte la lista de imágenes de entrenamiento en un array de NumPy y normaliza los valores de los píxeles.
test_images = np.array(test_images) / 255.0 #Convierte la lista de imágenes de prueba en un array de NumPy y normaliza los valores de los píxeles.

# Cambiar forma para adaptar a la entrada de la red (añadir una dimensión de canal)
train_images = train_images.reshape((train_images.shape[0], img_size, img_size, 1)) #Cambia la forma del array de imágenes de entrenamiento para incluir una dimensión de canal.
test_images = test_images.reshape((test_images.shape[0], img_size, img_size, 1)) #Cambia la forma del array de imágenes de prueba para incluir una dimensión de canal

# Etiquetas a formato categórico
train_labels = to_categorical(train_labels, num_classes=2) #Convierte las etiquetas de entrenamiento en formato binario.
test_labels = to_categorical(test_labels, num_classes=2) #Convierte las etiquetas de prueba en formato binario.

# Dividir datos de entrenamiento para validación
train_images, val_images, train_labels, val_labels = train_test_split( # Divide los datos de entrenamiento en conjuntos de entrenamiento y validación.
    train_images, train_labels, test_size=0.2, random_state=42)

# Crear el modelo mejorado
model = Sequential() #Crea un modelo secuencial con varias capas, incluyendo capas convolucionales,
# capas de normalización por lotes, capas de pooling, una capa de aplanamiento, capas densas, y una capa de salida.
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(img_size, img_size, 1)))#vCaptura patrones locales mediante la aplicación de filtros convolucionales.
model.add(MaxPooling2D((2, 2))) #Realiza operaciones de agrupación espacial.
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten()) #Transforma la salida de las capas anteriores en un vector unidimensional para la entrada a capas densas.
model.add(Dense(128, activation='relu'))#Captura patrones globales y relaciones no locales en la representación.
model.add(Dropout(0.5))  # Agregamos dropout para reducir el sobreajuste
model.add(Dense(2, activation='softmax'))  # 2 clases: Normal y Neumonía

# Compilar el modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Entrenar el modelo
history = model.fit(train_images, train_labels, epochs=15, validation_data=(val_images, val_labels))

# Evaluar el modelo
test_loss, test_acc = model.evaluate(test_images, test_labels)
print(f"Exactitud en Test: {test_acc}")

# Guardar el modelo
model.save('modelo_neumonia_mejorado2.tf')
