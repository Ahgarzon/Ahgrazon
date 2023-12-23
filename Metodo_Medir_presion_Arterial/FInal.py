import time
import pandas as pd
import numpy as np
import serial
from scipy.signal import find_peaks
import gspread
from google.oauth2.service_account import Credentials

# Configuración del puerto serial y la velocidad de baudios
PUERTO = 'COM4'  # Ajusta este valor según el puerto en el que está conectado tu Arduino
BAUDIOS = 9600
ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)

# Configuración de Google Sheets
creds = Credentials.from_service_account_file('presion-94a6b9048987.json')
scoped_creds = creds.with_scopes(['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
gc = gspread.authorize(scoped_creds)

nombre_hoja = 'Presion'
try:
    sh = gc.open(nombre_hoja)
except gspread.SpreadsheetNotFound:
    sh = gc.create(nombre_hoja)
    sh.share('agarzonsarzosa@gmail.com', perm_type='user', role='writer')

worksheet = sh.get_worksheet(0)

# DataFrame para almacenar los resultados
resultados = pd.DataFrame(columns=['Presión Sistólica', 'Presión Diastólica', 'Diagnóstico'])

# Funciones
def enviar_a_arduino(mensaje):
    ser.write(f"{mensaje}\n".encode())

def diagnostico_oms(sistolica, diastolica):
    if sistolica < 90 or diastolica < 60:
        return "Estado: hipotension"
    elif 90 <= sistolica <= 120 and 60 <= diastolica <= 80:
        return "Estado: normal"
    else:
        return "Estado: hipertension"

def agregar_resultado(sistolica, diastolica, diagnostico):
    global resultados
    index = len(resultados)
    resultados.loc[index] = [sistolica, diastolica, diagnostico]

def guardar_en_google_sheets():
    global resultados
    worksheet.append_rows(resultados.values.tolist())

# Bucle Principal
try:
    while True:
        datos_presion = []
        tiempos = []
        estabilizado = False
        tiempo_inicio_estabilizacion = None
        inicio_medicion = time.time()

        enviar_a_arduino("BIENVENIDO :)")

        # Proceso de inflado, desinflado y detección de picos sin cambios...
        # Proceso de inflado
        while True:
            if ser.in_waiting:
                dato = ser.readline().decode('utf-8').strip()
                try:
                    valor = float(dato)
                    tiempo_actual = time.time() - inicio_medicion
                    datos_presion.append(valor)
                    tiempos.append(tiempo_actual)

                    if not estabilizado and valor >= 122.35 - 0.5:
                        if tiempo_inicio_estabilizacion is None:
                            tiempo_inicio_estabilizacion = tiempo_actual
                            enviar_a_arduino("Comenzando a inflar...")
                        elif tiempo_actual - tiempo_inicio_estabilizacion >= 2:
                            estabilizado = True
                            enviar_a_arduino("Valor máximo estabilizado.")

                    if estabilizado and valor <= 122.35 - 0.5:
                        break

                except ValueError as e:
                    print(f"Error al convertir el dato: {e}")

        # Proceso de desinflado
        enviar_a_arduino("Desinflando...")
        while True:
            if ser.in_waiting:
                dato = ser.readline().decode('utf-8').strip()
                try:
                    valor = float(dato)
                    tiempo_actual = time.time() - inicio_medicion
                    datos_presion.append(valor)
                    tiempos.append(tiempo_actual)

                    if valor <= 14:
                        enviar_a_arduino("Desinflado completado.")
                        break

                except ValueError as e:
                    print(f"Error al convertir el dato: {e}")

        # Procesamiento de los datos para la detección de picos
        derivada_presion = np.diff(datos_presion) / np.diff(tiempos)
        derivada_presion = np.insert(derivada_presion, 0, 0)
        picos_derivada, _ = find_peaks(abs(derivada_presion), height=np.std(derivada_presion))

        if tiempo_inicio_estabilizacion is not None:
            picos_derivada = [p for p in picos_derivada if tiempos[p] >= tiempo_inicio_estabilizacion + 2]

            # Asegúrate de que los picos se detecten correctamente
            if len(picos_derivada) > 0:
                pico_sistolico = picos_derivada[0]
                presion_sistolica = datos_presion[pico_sistolico]
                presion_diastolica = datos_presion[pico_sistolico] * 0.67  # Ajusta si es necesario
                diagnostico = diagnostico_oms(presion_sistolica, presion_diastolica)
                mensaje_presiones = f"{round(presion_sistolica)} | {round(presion_diastolica)} | {diagnostico}"
                enviar_a_arduino(mensaje_presiones)
                agregar_resultado(presion_sistolica, presion_diastolica, diagnostico)
                guardar_en_google_sheets()
            else:
                mensaje_error = "No se detectó presión sistólica"
                print(mensaje_error)
                enviar_a_arduino(mensaje_error)
        else:
            print("Error: Tiempos iguales detectados, evitando división por cero.")

        time.sleep(10)
except Exception as e:
    print(f"Se produjo un error: {e}")
finally:
    ser.close()
