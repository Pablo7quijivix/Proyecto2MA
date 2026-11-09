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
        btn_modificar.grid(row=7, column=0, pady=4, padx=5, sticky="ew")

        btn_eliminar = tk.Button(frame, text="Eliminar Contacto", bg="#D32F2F", fg="white", width=16, command=lambda: self.ejecutar_opcion_menu("eliminar"))
        btn_eliminar.grid(row=7, column=1, pady=4, padx=5, sticky="ew")

        btn_limpiar = tk.Button(frame, text="Limpiar", bg="#FFEB3B", fg="black", width=16, command=lambda: self.ejecutar_opcion_menu("limpiar"))
        btn_limpiar.grid(row=8, column=0, pady=4, padx=5, sticky="ew")

        btn_cargar = tk.Button(frame, text="Cargar datos", bg="#607D8B", fg="white", width=16, command=lambda: self.ejecutar_opcion_menu("cargar_datos"))
        btn_cargar.grid(row=8, column=1, pady=4, padx=5, sticky="ew")

        # Visor de Contactos (Tabla ttk.Treeview)
        lbl_visor = tk.Label(frame, text="Visor de Contactos", font=("Arial", 10, "bold"))
        lbl_visor.grid(row=9, column=0, columnspan=2, sticky="w", padx=10, pady=(8, 2))

        columnas = ("ID", "Nombre", "Teléfono", "Correo", "Ciudad")
        self.tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=7)
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=110, anchor="w")
            
        self.tabla.grid(row=10, column=0, columnspan=4, padx=10, pady=2, sticky="nsew")

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=10, column=4, sticky="ns", pady=2)

        self.cargar_tabla()

    def cargar_tabla(self):
        # Actualiza y carga todos los registros actuales dentro de la tabla visor.
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        
        contactos = self.contact_manager.obtener_todos()
        for c in contactos:
            self.tabla.insert("", "end", values=(c["id"], c["nombre"], c["telefono"], c["correo"], c["ciudad"]))

    def accion_agregar(self):
        # Valida los campos, agrega el contacto y actualiza el visor en tabla.
        try:
            id_val = int(self.entries["id"].get().strip())
            nombre = self.entries["nombre"].get().strip()
            telefono = self.entries["telefono"].get().strip()
            correo = self.entries["correo"].get().strip()
            ciudad = self.entries["ciudad"].get().strip()

            if not nombre or not telefono or not correo or not ciudad:
                raise ValueError("Todos los campos son obligatorios.")
            if not telefono.isdigit():
                raise ValueError("El teléfono solo debe contener números.")

            self.contact_manager.agregar_contacto(id_val, nombre, telefono, correo, ciudad)
            messagebox.showinfo("Éxito", "Contacto agregado correctamente.")
            self.limpiar_campos()
            self.cargar_tabla()
        except Exception as e:
            messagebox.showerror("Error de Validación", str(e))

    def accion_buscar(self):
        # Busca un contacto por ID limpiando posibles espacios o caracteres invisibles.
        try:
            texto_id = self.entries["id"].get().strip()
            if not texto_id:
                raise ValueError("El campo ID está vacío.")
            
            id_val = int(texto_id)
            contacto = self.contact_manager.buscar_por_id(id_val)
            
            if contacto:
                self.entries["nombre"].delete(0, tk.END)
                self.entries["nombre"].insert(0, contacto["nombre"])
                self.entries["telefono"].delete(0, tk.END)
                self.entries["telefono"].insert(0, contacto["telefono"])
                self.entries["correo"].delete(0, tk.END)
                self.entries["correo"].insert(0, contacto["correo"])
                self.entries["ciudad"].delete(0, tk.END)
                self.entries["ciudad"].insert(0, contacto["ciudad"])
                messagebox.showinfo("Encontrado", f"Contacto encontrado mediante acceso aleatorio (ID: {id_val}).")
            else:
                messagebox.showwarning("No encontrado", f"El ID {id_val} no existe en el sistema.")
        except ValueError as e:
            msg = str(e) if "vacío" in str(e) else "El ID debe ser un número entero válido."
            messagebox.showerror("Error", msg)

    def accion_modificar(self):
        # Modifica un registro existente y refresca la tabla.
        try:
            id_val = int(self.entries["id"].get().strip())
            nombre = self.entries["nombre"].get().strip()
            telefono = self.entries["telefono"].get().strip()
            correo = self.entries["correo"].get().strip()
            ciudad = self.entries["ciudad"].get().strip()

            if not telefono.isdigit():
                raise ValueError("El teléfono solo debe contener números.")

            self.contact_manager.modificar_contacto(id_val, nombre, telefono, correo, ciudad)
            messagebox.showinfo("Éxito", f"Contacto con ID {id_val} modificado correctamente en el lugar.")
            self.cargar_tabla()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def accion_eliminar(self):
        # Elimina un contacto basándose en el ID ingresado tras una confirmación de seguridad.
        try:
            texto_id = self.entries["id"].get().strip()
            if not texto_id:
                raise ValueError("Ingrese el ID del contacto que desea eliminar.")
            
            id_val = int(texto_id)
            
            # Pide confirmación al usuario
            confirmar = messagebox.askyesno("Confirmar Eliminación", f"¿Está seguro de eliminar el contacto con ID {id_val}?")
            if not confirmar:
                return

            self.contact_manager.eliminar_contacto(id_val)
            messagebox.showinfo("Éxito", f"Contacto con ID {id_val} eliminado correctamente.")
            self.limpiar_campos()
            self.cargar_tabla()
        except Exception as e:
            messagebox.showerror("Error de Eliminación", str(e))

    def limpiar_campos(self):
        # Vacía todas las cajas de texto de la interfaz para un nuevo ingreso.
        for ent in self.entries.values():
            ent.delete(0, tk.END)

    def accion_cargar_datos(self):
        # Abre un diálogo de archivos para seleccionar un archivo externo (.txt o .csv) y realizar la carga masiva.
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de datos",
            filetypes=[("Archivos de texto y CSV", "*.txt *.csv"), ("Todos los archivos", "*.*")]
        )
        if not ruta_archivo:
            return

        try:
            cargados, errores = self.cargador_datos.procesar_archivo_externo(ruta_archivo)
            msg = f"Se cargaron exitosamente {cargados} registros."
            if errores:
                msg += f"\n\nHubo {len(errores)} errores o registros duplicados omitidos."
            messagebox.showinfo("Carga Masiva Finalizada", msg)
            self.cargar_tabla()
        except Exception as e:
            messagebox.showerror("Error de Carga", f"Ocurrió un error al procesar el archivo:\n{str(e)}")

    def construir_pestana_exportar(self):
        # Diseña la pestaña de exportación.
        frame = self.tab_exportar
        lbl = tk.Label(frame, text="Opciones de Exportación", font=("Arial", 11, "bold"))
        lbl.pack(pady=20)

        btn_json = tk.Button(frame, text="Exportar a JSON", width=25, bg="#009688", fg="white", command=lambda: self.ejecutar_opcion_menu("exportar_json"))
        btn_json.pack(pady=10)

        btn_pdf = tk.Button(frame, text="Generar Reporte PDF", width=25, bg="#E91E63", fg="white", command=lambda: self.ejecutar_opcion_menu("exportar_pdf"))
        btn_pdf.pack(pady=10)

    def accion_exportar_json(self):
        contactos = self.contact_manager.obtener_todos()
        ruta = self.exporter.exportar_json(contactos)
        messagebox.showinfo("Exportado", f"Archivo JSON generado exitosamente en:\n{ruta}")

    def accion_exportar_pdf(self):
        contactos = self.contact_manager.obtener_todos()
        ruta = self.exporter.exportar_pdf(contactos)
        messagebox.showinfo("Reporte PDF", f"Reporte PDF generado exitosamente en:\n{ruta}")

    def construir_pestana_herramientas(self):
        # Diseña la pestaña de herramientas.
        frame = self.tab_herramientas
        lbl = tk.Label(frame, text="Herramientas del Sistema", font=("Arial", 11, "bold"))
        lbl.pack(pady=20)

        btn_integ = tk.Button(frame, text="Verificar Integridad SHA-256", width=30, command=lambda: self.ejecutar_opcion_menu("verificar_integridad"))
        btn_integ.pack(pady=8)

        btn_zip = tk.Button(frame, text="Crear Respaldo ZIP", width=30, command=lambda: self.ejecutar_opcion_menu("respaldo_zip"))
        btn_zip.pack(pady=8)

        btn_info = tk.Button(frame, text="Información del Archivo", width=30, command=lambda: self.ejecutar_opcion_menu("info_archivo"))
        btn_info.pack(pady=8)

    def accion_verificar_integridad(self):
        valido = self.contact_manager.verificar_integridad()
        if valido:
            messagebox.showinfo("Integridad OK", "El archivo de contactos es íntegro y no ha sido alterado.")
        else:
            messagebox.showwarning("Alerta", "El archivo ha sido modificado externamente.")

    def accion_respaldo_zip(self):
        ruta_zip, orig, comp = self.contact_manager.crear_respaldo_zip()
        messagebox.showinfo("Respaldo Creado", f"Respaldo guardado en: {ruta_zip}\nTamaño original: {orig} bytes\nTamaño comprimido: {comp} bytes")

    def accion_info_archivo(self):
        meta = self.contact_manager.obtener_metadatos_archivo()
        if "error" in meta:
            messagebox.showerror("Error", meta["error"])
        else:
            msg = (f"Tamaño: {meta['tamano_bytes']} bytes\n"
                   f"Última modificación: {meta['ultima_modificacion']}\n"
                   f"Permiso de lectura: {'Sí' if meta['lectura'] else 'No'}\n"
                   f"Permiso de escritura: {'Sí' if meta['escritura'] else 'No'}")
            messagebox.showinfo("Información del Archivo", msg)

    def construir_pestana_ayuda(self):
        # Diseña la pestaña de ayuda.
        frame = self.tab_ayuda
        lbl = tk.Label(frame, text="Ayuda del Sistema (Simulado)", font=("Arial", 11, "bold"))
        lbl.pack(pady=20)
        txt = tk.Label(frame, text="Esta aplicación administra una agenda de contactos mediante\n"
                                   "registros de tamaño fijo de 100 caracteres, acceso aleatorio seek(),\n"
                                   "índice primario JSON, verificación SHA-256 y respaldos ZIP.\n\n"
                                   "Para soporte adicional, contacte al administrador del sistema.", justify="center")
        lbl_trade = tk.Label(frame, text="Sacrificado: Espacio adicional para índices y tablas hash.\n"
                                         "Obteniendo: Búsqueda y acceso aleatorio en O(1).", font=("Arial", 9, "italic"), fg="#555")
        txt.pack(pady=10)
        lbl_trade.pack(pady=10)