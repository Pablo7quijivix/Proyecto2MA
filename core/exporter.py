# Módulo para la exportación de información a formatos JSON y PDF, 
# incluyendo la generación automática del reporte de eficiencia y análisis de Trade-Off.

import os
import json
from datetime import datetime
from fpdf import FPDF

class Exporter:
    def __init__(self):
        # Inicializa las rutas de exportación para los reportes.
        self.dir_json = "archivos_generados/JSON"
        self.dir_pdf = "archivos_generados/PDF"
        self.dir_eficiencia = "Eficiencia"

    def exportar_json(self, contactos):
        # Exporta la lista completa de contactos a un archivo JSON estructurado.
        ruta = os.path.join(self.dir_json, "contactos_exportados.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(contactos, f, ensure_ascii=False, indent=4)
        return ruta

    def exportar_pdf(self, contactos):
        # Genera un reporte PDF formal de la agenda de contactos con fecha de generación usando FPDF2.
        ruta = os.path.join(self.dir_pdf, "reporte_contactos.pdf")
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("helvetica", "B", 16)
        
        pdf.cell(0, 10, "Reporte de Agenda de Contactos", ln=True, align="C")
        pdf.set_font("helvetica", "", 10)
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pdf.cell(0, 10, f"Fecha de generación: {fecha_actual}", ln=True, align="C")
        pdf.ln(10)
        
        # Cabecera de la tabla
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(15, 8, "ID", 1)
        pdf.cell(45, 8, "Nombre", 1)
        pdf.cell(35, 8, "Teléfono", 1)
        pdf.cell(55, 8, "Correo", 1)
        pdf.cell(40, 8, "Ciudad", 1)
        pdf.ln()
        
        # Filas de la tabla
        pdf.set_font("helvetica", "", 9)
        for c in contactos:
            pdf.cell(15, 8, str(c["id"]), 1)
            pdf.cell(45, 8, str(c["nombre"]), 1)
            pdf.cell(35, 8, str(c["telefono"]), 1)
            pdf.cell(55, 8, str(c["correo"]), 1)
            pdf.cell(40, 8, str(c["ciudad"]), 1)
            pdf.ln()
            
        pdf.output(ruta)
        return ruta
