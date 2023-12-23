import cv2
import numpy as np
from scipy import ndimage as ndi

# Inicializar la captura de la cámara (cambiar el índice según sea necesario)
cap = cv2.VideoCapture(0)

# Umbral de área mínimo para filtrar objetos pequeños
min_area_threshold = 200

while True:
    # Capturar un frame
    ret, frame = cap.read()

    # Dividir el frame en los planos de color BGR
    B, G, R = cv2.split(frame)

    # Umbralizar cada plano de color
    levelb = 102
    levelg = 127
    levelr = 155

    i1 = cv2.threshold(B, levelb, 255, cv2.THRESH_BINARY)[1]
    i2 = cv2.threshold(G, levelg, 255, cv2.THRESH_BINARY)[1]
    i3 = cv2.threshold(R, levelr, 255, cv2.THRESH_BINARY)[1]

    # Suma de todos los planos
    Isum = cv2.bitwise_and(i1, cv2.bitwise_and(i2, i3))

    # Imagen complemento y relleno de agujeros
    Icomp = cv2.bitwise_not(Isum)
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    Iclose = cv2.morphologyEx(Icomp, cv2.MORPH_CLOSE, se, iterations=3)

    Ifilled = ndi.binary_fill_holes(Iclose)
    Ifilled = Ifilled.astype('uint8') * 255
    Ifilled = cv2.morphologyEx(Ifilled, cv2.MORPH_OPEN, se, iterations=2)

    # Extraer objetos y medir tamaño y dimensiones
    numObjects, labeled, stats, centroids = cv2.connectedComponentsWithStats(Ifilled)

    # Crear una imagen para mostrar los tamaños y dimensiones de los objetos
    sizes_image = np.copy(frame)
    font = cv2.FONT_HERSHEY_SIMPLEX
    for i in range(1, numObjects):
        x, y, w, h, area = stats[i]

        # Filtrar objetos pequeños usando el umbral de área
        if area >= min_area_threshold:
            cv2.rectangle(sizes_image, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Mostrar las medidas dentro del rectángulo
            cv2.putText(sizes_image, f'Object {i}: {w}x{h} pixels',
                        (x, y - 10), font, 0.5, (255, 0, 0), 1)

    # Mostrar la imagen con los resultados
    cv2.imshow('Object Sizes and Dimensions', sizes_image)

    # Salir del bucle si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura y cerrar ventanas
cap.release()
cv2.destroyAllWindows()

