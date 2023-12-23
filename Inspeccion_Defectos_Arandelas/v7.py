import cv2
import numpy as np
import time

# Inicializa la captura de video
cap = cv2.VideoCapture('Aralndelaa.mp4')

# Umbral de dimensiones para clasificar las arandelas
min_dimension_good = (220, 220)
max_dimension_good = (250, 250)
min_dimension_defective = (180, 180)
max_dimension_defective = (219, 219)

# Define un umbral mínimo de área para los objetos a considerar
min_area_threshold = 270

# Inicializa el contador de arandelas buenas y defectuosas
good_washers_count = 0
defective_washers_count = 0

# Tiempo de retardo para considerar una arandela buena o defectuosa (0.7 segundos)
washer_delay = 0.9
last_washer_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        # Convertir a escala de grises y binarizar la imagen
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

        # Aplicar connectedComponentsWithStats
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)

        # Dibujar línea de interés
        height, width = frame.shape[:2]
        mid_x = width // 2
        cv2.line(frame, (mid_x, 0), (mid_x, height), (0, 255, 0), 2)

        # Iterar a través de los componentes conectados
        for i in range(1, num_labels):
            x, y, w, h, area = stats[i]
            if area >= min_area_threshold:
                within_good_range = min_dimension_good[0] <= w <= max_dimension_good[0] and min_dimension_good[1] <= h <= max_dimension_good[1]
                within_defective_range = min_dimension_defective[0] <= w <= max_dimension_defective[0] and min_dimension_defective[1] <= h <= max_dimension_defective[1]

                if mid_x >= x and mid_x <= x + w:
                    if within_good_range:
                        text = 'Buena'
                        color = (0, 255, 0)
                        if time.time() - last_washer_time >= washer_delay:
                            good_washers_count += 1
                            last_washer_time = time.time()
                    elif within_defective_range:
                        text = 'Defectuosa'
                        color = (0, 0, 255)
                        if time.time() - last_washer_time >= washer_delay:
                            defective_washers_count += 1
                            last_washer_time = time.time()
                    else:
                        continue  # Si no está dentro de ningún rango, continúa con el siguiente componente

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, f'{text}: {w}x{h}', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # Dibujar los contadores en la pantalla
        cv2.putText(frame, f'Arandelas Buenas: {good_washers_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, f'Arandelas Defectuosas: {defective_washers_count}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Muestra la imagen en una ventana
        cv2.imshow('Inspección', frame)

        # Salir con 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Limpieza
cap.release()
cv2.destroyAllWindows()
