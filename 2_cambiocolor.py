import numpy as np
import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    # Capturar frame por frame
    ret, frame = cap.read()

    # Convertir de BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Definir el rango de color verde en HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])

    # Crear una máscara usando inRange
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    # Bitwise-AND para obtener solo los píxeles verdes de la imagen original
    result_green = cv2.bitwise_and(frame, frame, mask=mask_green)

    # Cambiar el color verde a rojo
    result_red = frame.copy()
    result_red[mask_green > 0] = [0, 0, 255]  # Cambiar los píxeles verdes a rojo

    # Mostrar la imagen resultante en verde
    cv2.imshow('deteccion de color verde', result_green)

    # Mostrar la imagen resultante en rojo
    cv2.imshow('verde a rojo', result_red)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cuando todo esté hecho, liberar la captura
cap.release()
cv2.destroyAllWindows()
