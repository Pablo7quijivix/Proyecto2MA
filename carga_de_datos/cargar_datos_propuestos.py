# Módulo encargado de la lectura, conversión y carga masiva de datos desde archivos externos 
# (como .txt o .csv) al formato de texto plano de tamaño fijo requerido por el sistema.

import os
import csv

class CargarDatosPropuestos:
    def __init__(self, contact_manager):
        # Inicializa el componente con una instancia del gestor de contactos del sistema.
        self.contact_manager = contact_manager

    def procesar_archivo_externo(self, ruta_archivo):
        # Lee un archivo externo en formato txt o csv, extrae los campos y los registra en el sistema validando restricciones.
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"No se encontró el archivo en la ruta: {ruta_archivo}")

        registros_cargados = 0
        errores = []

        ext = os.path.splitext(ruta_archivo)[1].lower()

        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            if ext == '.csv':
                lector = csv.reader(f)
                lineas = [row for row in lector if row]
            else:
                lineas = []
                for linea in f:
                    linea_limpia = linea.strip()
                    if linea_limpia:
                        partes = [p.strip() for p in linea_limpia.replace('\t', ',').split(',')]
                        lineas.append(partes)

            for idx, campos in enumerate(lineas):
                try:
                    if len(campos) < 5:
                        continue
                    
                    id_val = int(campos[0])
                    nombre = campos[1]
                    telefono = campos[2]
                    correo = campos[3]
                    ciudad = campos[4]

                    # Valida y registra utilizando la lógica principal del sistema
                    self.contact_manager.agregar_contacto(id_val, nombre, telefono, correo, ciudad)
                    registros_cargados += 1
                except Exception as e:
                    errores.append(f"Línea {idx+1}: {str(e)}")

        return registros_cargados, errores