# Módulo encargado de gestionar el índice primario en formato JSON para relacionar IDs con números de registro.
# Permite búsquedas rápidas en memoria y persistencia automática en disco.

import os
import json

class IndexManager:
    def __init__(self):
        # Define la ruta del archivo de índice JSON.
        self.ruta_indice = "archivos_generados/JSON/indice.json"
        self.indice = {}
        self.cargar_indice()

    def cargar_indice(self):
        # Carga el índice desde el archivo JSON si existe; de lo contrario, inicializa un diccionario vacío.
        if os.path.exists(self.ruta_indice):
            try:
                with open(self.ruta_indice, "r", encoding="utf-8") as f:
                    data = f.read()
                    if data:
                        # Asegura que todas las llaves se carguen como enteros
                        self.indice = {int(k): int(v) for k, v in json.loads(data).items()}
            except Exception:
                self.indice = {}

    def guardar_indice(self):
        # Persiste el índice actual en el archivo JSON en UTF-8.
        with open(self.ruta_indice, "w", encoding="utf-8") as f:
            json.dump(self.indice, f, ensure_ascii=False, indent=4)

    def agregar(self, id_val, num_registro):
        # Agrega o actualiza una entrada en el índice y guarda los cambios en disco.
        self.indice[int(id_val)] = int(num_registro)
        self.guardar_indice()

    def buscar(self, id_val):
        # Busca y retorna el número de registro asociado a un ID utilizando la estructura de diccionario (Tabla Hash).
        return self.indice.get(int(id_val))