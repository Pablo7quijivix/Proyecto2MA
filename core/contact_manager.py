# Módulo de lógica de negocio para la administración de contactos en archivos de tamaño fijo.
# Permite agregar, buscar, modificar y eliminar registros directamente mediante acceso aleatorio y control de integridad hash.

import os
import hashlib
import zipfile
import unicodedata
from core.index_manager import IndexManager

class ContactManager:
    # Estructura que define el tamaño y longitud de cada campo dentro del registro de tamaño fijo.
    TAMANO_ID = 5
    TAMANO_NOMBRE = 30
    TAMANO_TELEFONO = 15
    TAMANO_CORREO = 30
    TAMANO_CIUDAD = 20
    TAMANO_REGISTRO = TAMANO_ID + TAMANO_NOMBRE + TAMANO_TELEFONO + TAMANO_CORREO + TAMANO_CIUDAD # Total: 100 bytes

    def __init__(self):
        # Inicializa las rutas de los archivos de datos e índice principal.
        self.ruta_dat = "archivos_generados/DAT/contactos.dat"
        self.ruta_hash = "archivos_generados/SHA256/contactos.sha256"
        self.index_manager = IndexManager()
        self.inicializar_archivo()

    def inicializar_archivo(self):
        # Verifica la existencia del archivo de datos; si no existe, lo crea vacío.
        if not os.path.exists(self.ruta_dat):
            with open(self.ruta_dat, "w", encoding="utf-8") as f:
                pass
            self.actualizar_hash()

    def limpiar_texto(self, texto):
        # Remueve tildes y caracteres especiales para garantizar byte a byte la consistencia de tamaño fijo.
        if not texto:
            return ""
        nfkd_form = unicodedata.normalize('NFKD', str(texto))
        return "".join([c for c in nfkd_form if not unicodedata.combining(c)])

    def calcular_hash(self):
        # Calcula y retorna el hash SHA-256 del archivo de contactos actual para verificar su integridad.
        hasher = hashlib.sha256()
        if os.path.exists(self.ruta_dat):
            with open(self.ruta_dat, "rb") as f:
                buf = f.read()
                hasher.update(buf)
        return hasher.hexdigest()

    def actualizar_hash(self):
        # Guarda el hash SHA-256 actual en su archivo correspondiente.
        digest = self.calcular_hash()
        with open(self.ruta_hash, "w", encoding="utf-8") as f:
            f.write(digest)

    def verificar_integridad(self):
        # Compara el hash almacenado con el hash actual del archivo para detectar modificaciones externas.
        if not os.path.exists(self.ruta_hash):
            return True
        with open(self.ruta_hash, "r", encoding="utf-8") as f:
            hash_guardado = f.read().strip()
        hash_actual = self.calcular_hash()
        return hash_guardado == hash_actual

    def serializar_registro(self, id_val, nombre, telefono, correo, ciudad):
        # Formatea y ajusta los campos a una longitud fija exacta normalizando acentos.
        s_id = str(id_val).ljust(self.TAMANO_ID)[:self.TAMANO_ID]
        s_nom = self.limpiar_texto(nombre).ljust(self.TAMANO_NOMBRE)[:self.TAMANO_NOMBRE]
        s_tel = str(telefono).ljust(self.TAMANO_TELEFONO)[:self.TAMANO_TELEFONO]
        s_cor = self.limpiar_texto(correo).ljust(self.TAMANO_CORREO)[:self.TAMANO_CORREO]
        s_ciu = self.limpiar_texto(ciudad).ljust(self.TAMANO_CIUDAD)[:self.TAMANO_CIUDAD]
        
        return s_id + s_nom + s_tel + s_cor + s_ciu

    def agregar_contacto(self, id_val, nombre, telefono, correo, ciudad):
        # Agrega un nuevo contacto validando que el ID no exista previamente.
        if self.index_manager.buscar(id_val) is not None:
            raise ValueError(f"El ID {id_val} ya existe en el sistema.")
        
        registro = self.serializar_registro(id_val, nombre, telefono, correo, ciudad)
        
        with open(self.ruta_dat, "ab") as f:
            f.write(registro.encode('latin-1'))
        
        tam_archivo = os.path.getsize(self.ruta_dat)
        num_registro = (tam_archivo // self.TAMANO_REGISTRO) - 1

        self.index_manager.agregar(id_val, num_registro)
        self.actualizar_hash()

    def buscar_por_id(self, id_val):
        # Busca un contacto consultando el índice y utilizando seek() binario para acceso aleatorio O(1).
        num_reg = self.index_manager.buscar(id_val)
        if num_reg is None:
            return None

        with open(self.ruta_dat, "rb") as f:
            f.seek(num_reg * self.TAMANO_REGISTRO)
            data_bytes = f.read(self.TAMANO_REGISTRO)
            
        if not data_bytes or len(data_bytes) < self.TAMANO_REGISTRO:
            return None

        data = data_bytes.decode('latin-1', errors='ignore')
        # Si el ID está marcado como eliminado (ej. espacios), retorna None
        if not data[:self.TAMANO_ID].strip():
            return None

        contacto = {
            "id": int(data[:self.TAMANO_ID].strip()),
            "nombre": data[self.TAMANO_ID:self.TAMANO_ID+self.TAMANO_NOMBRE].strip(),
            "telefono": data[self.TAMANO_ID+self.TAMANO_NOMBRE:self.TAMANO_ID+self.TAMANO_NOMBRE+self.TAMANO_TELEFONO].strip(),
            "correo": data[self.TAMANO_ID+self.TAMANO_NOMBRE+self.TAMANO_TELEFONO:self.TAMANO_ID+self.TAMANO_NOMBRE+self.TAMANO_TELEFONO+self.TAMANO_CORREO].strip(),
            "ciudad": data[self.TAMANO_ID+self.TAMANO_NOMBRE+self.TAMANO_TELEFONO+self.TAMANO_CORREO:].strip()
        }
        return contacto