# Módulo de interfaz gráfica desarrollado con Tkinter. 
# Implementa el menú principal, controles avanzados, visor en tabla y enrutamiento por match case.

import os
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from core.contact_manager import ContactManager
from core.exporter import Exporter
from carga_de_datos.cargar_datos_propuestos import CargarDatosPropuestos

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión de Agenda - Acceso Aleatorio")
        self.geometry("800x680")
        self.config(bg="#f0f2f5")

        self.contact_manager = ContactManager()
        self.exporter = Exporter()
        self.cargador_datos = CargarDatosPropuestos(self.contact_manager)
        
        # Genera automáticamente el reporte PDF de eficiencia al iniciar el sistema
        self.exporter.generar_pdf_eficiencia()
        
        self.crear_interfaz()
        self.verificar_integridad_inicial()

    def verificar_integridad_inicial(self):
        # Verifica al iniciar si el archivo de contactos fue alterado externamente.
        if not self.contact_manager.verificar_integridad():
            messagebox.showwarning(
                "Alerta de Integridad",
                "¡Atención! El archivo de contactos fue modificado fuera de la aplicación (el hash SHA-256 no coincide)."
            )

    def crear_interfaz(self):
        # Crea los componentes visuales de la ventana principal y la barra de navegación por pestañas.
        titulo = tk.Label(self, text="Administrador de Agenda de Contactos", font=("Arial", 16, "bold"), bg="#f0f2f5", fg="#333")
        titulo.pack(pady=10)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=15, pady=5)

        self.tab_contactos = ttk.Frame(self.notebook)
        self.tab_exportar = ttk.Frame(self.notebook)
        self.tab_herramientas = ttk.Frame(self.notebook)
        self.tab_ayuda = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_contactos, text="Contactos")
        self.notebook.add(self.tab_exportar, text="Exportar")
        self.notebook.add(self.tab_herramientas, text="Herramientas")
        self.notebook.add(self.tab_ayuda, text="Ayuda")

        self.construir_pestana_contactos()
        self.construir_pestana_exportar()
        self.construir_pestana_herramientas()
        self.construir_pestana_ayuda()

    def ejecutar_opcion_menu(self, opcion, *args):
        # Ejecuta la acción correspondiente utilizando match case según la opción seleccionada del menú.
        match opcion:
            case "agregar":
                return self.accion_agregar(*args)
            case "buscar":
                return self.accion_buscar(*args)
            case "modificar":
                return self.accion_modificar(*args)
            case "eliminar":
                return self.accion_eliminar(*args)
            case "limpiar":
                return self.limpiar_campos()
            case "cargar_datos":
                return self.accion_cargar_datos()
            case "exportar_json":
                return self.accion_exportar_json()
            case "exportar_pdf":
                return self.accion_exportar_pdf()
            case "verificar_integridad":
                return self.accion_verificar_integridad()
            case "respaldo_zip":
                return self.accion_respaldo_zip()
            case "info_archivo":
                return self.accion_info_archivo()
            case _:
                messagebox.showerror("Error", "Opción de menú no reconocida.")

    def construir_pestana_contactos(self):
        # Diseña los formularios, botones de acción y la tabla visor de registros.
        frame = self.tab_contactos
        
        lbl_info = tk.Label(frame, text="Gestión de Contactos (ID único, tamaño fijo)", font=("Arial", 11, "bold"))
        lbl_info.grid(row=0, column=0, columnspan=4, pady=6)

        labels = ["ID (Entero):", "Nombre:", "Teléfono:", "Correo:", "Ciudad:"]
        self.entries = {}

        for idx, texto in enumerate(labels):
            lbl = tk.Label(frame, text=texto)
            lbl.grid(row=idx+1, column=0, sticky="w", padx=10, pady=3)
            ent = tk.Entry(frame, width=28)
            ent.grid(row=idx+1, column=1, padx=10, pady=3, sticky="w")
            key = texto.split()[0].lower().replace(":", "").replace("é", "e")
            self.entries[key] = ent

        # Botones de operación distribuidos ordenadamente
        btn_agregar = tk.Button(frame, text="Agregar Contacto", bg="#4CAF50", fg="white", width=16, command=lambda: self.ejecutar_opcion_menu("agregar"))
        btn_agregar.grid(row=6, column=0, pady=6, padx=5, sticky="ew")

        btn_buscar = tk.Button(frame, text="Buscar por ID", bg="#2196F3", fg="white", width=16, command=lambda: self.ejecutar_opcion_menu("buscar"))
        btn_buscar.grid(row=6, column=1, pady=6, padx=5, sticky="ew")

        btn_modificar = tk.Button(frame, text="Modificar Contacto", bg="#FF9800", fg="white", width=16, command=lambda: self.ejecutar_opcion_menu("modificar"))