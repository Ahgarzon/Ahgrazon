import cv2
import numpy as np
from scipy import ndimage as ndi

# Definir el umbral mínimo de área
min_area_threshold = 180

# Inicializar la captura de la cámara (cambiar el índice según sea necesario)
cap = cv2.VideoCapture(0)

while True:
    # Capturar un cuadro del video
    ret, frame = cap.read()
    if not ret:
        break

    # Dividir el cuadro en los planos de color BGR
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

    # Extraer objetos y clasificar formas
    numObjects, labeled, stats, centroids = cv2.connectedComponentsWithStats(Ifilled) #Devuelve el numero de objetos, una imagen etiquetada de cada pixel, estadisticas del objeto y las cordenadas del centroide.

    for i in range(1, numObjects): #para interar con cada objeto
        x, y, w, h, area = stats[i] # scamos de la funcion stats la cordenada de las esquinas, el ancho, altura y finalmente el area del objeto

        # Filtrar objetos pequeños usando el umbral de área
        if area >= min_area_threshold: #compara si el area del objeto es mayor que el umbral definido
            # Encontrar el contorno de la región etiquetada
            contour, _ = cv2.findContours((labeled == i).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #recupera los contornos extremos del objeto

            # Calcular la longitud del arco del contorno
            epsilon = 0.04 * cv2.arcLength(contour[0], True) #aproximacion de poligonos, calcula la longitud del arco del contorno, 0.04 para ajustar la aproximacion
            approx = cv2.approxPolyDP(contour[0], epsilon, True) #indica si la aproximacion es cerrada y simplifica el corntorno original, aproxx da los vertices

            # Clasificar formas
            if len(approx) == 3: #si la longitud del poligono aproximado es 3
                forma = "Triángulo"
            elif len(approx) == 4:
                forma = "Cuadrado"
            else:
                forma = "Círculo" #lo demas es circulo

            # Dibujar el recuadro alrededor del objeto
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) # la imgane orginonal, las cordenadas de los vetices, el color y borde del rectaungulo

            # Mostrar la clasificación de forma dentro del recuadro
            font = cv2.FONT_HERSHEY_SIMPLEX # el tipo de fuente
            cv2.putText(frame, forma, (x, y - 10), font, 0.5, (255, 0, 0), 1) #propiedades del texto

    # Mostrar el cuadro con los resultados en tiempo real
    cv2.imshow('clasificacion de formas', frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
