# Módulo principal para la ejecución de la aplicación de escritorio.
# Se encarga de inicializar los directorios base y lanzar la interfaz gráfica principal.

import os
from ui.main_window import MainApplication

def asegurar_directorios():
    # Crea la estructura de directorios y subcarpetas necesarias para la persistencia y reportes.
    directorios = [
        "archivos_generados/DAT",
        "archivos_generados/JSON",
        "archivos_generados/PDF",
        "archivos_generados/SHA256",
        "archivos_generados/ZIP",
        "Eficiencia"
    ]
    for directorio in directorios:
        os.makedirs(directorio, exist_ok=True)

if __name__ == "__main__":
    asegurar_directorios()
    app = MainApplication()
    app.mainloop()