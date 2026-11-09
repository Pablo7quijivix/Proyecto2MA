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
    
    def generar_pdf_eficiencia(self):
        # Genera el archivo PDF con la tabla de complejidad temporal y la sección detallada de Trade-Off.
        ruta = os.path.join(self.dir_eficiencia, "reporte_eficiencia.pdf")
        pdf = FPDF()
        pdf.add_page()
        
        # Título
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, "Análisis de Complejidad Temporal y Trade-Off", ln=True, align="C")
        pdf.ln(5)
        
        # Sección 1: Complejidad Temporal
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 8, "1. Complejidad Temporal (Big O / Notación O grande)", ln=True)
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(190, 6, "Comparación de escalabilidad del tiempo de ejecución al aumentar el tamaño de entrada (n):")
        pdf.ln(3)
        
        # Tabla Big O
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(40, 8, "n", 1)
        pdf.cell(50, 8, "O(n)", 1)
        pdf.cell(50, 8, "O(n^2)", 1)
        pdf.cell(50, 8, "O(log n)", 1)
        pdf.ln()
        
        pdf.set_font("helvetica", "", 10)
        datos_big_o = [
            ("10", "10", "100", "3"),
            ("1,000", "1,000", "1,000,000", "10")
        ]
        for fila in datos_big_o:
            pdf.cell(40, 8, fila[0], 1)
            pdf.cell(50, 8, fila[1], 1)
            pdf.cell(50, 8, fila[2], 1)
            pdf.cell(50, 8, fila[3], 1)
            pdf.ln()
            
        pdf.ln(10)
        
        # Sección 2: Trade-Off
        pdf.set_font("helvetica", "B", 11)
        pdf.cell(0, 8, "2. Trade-Off (Compromiso Espacio-Tiempo)", ln=True)
        pdf.set_font("helvetica", "", 9)
        
        # Tabla Trade-Off
        pdf.set_font("helvetica", "B", 9)
        pdf.cell(40, 8, "Estructura", 1)
        pdf.cell(70, 8, "¿Qué sacrifica?", 1)
        pdf.cell(80, 8, "¿Qué obtiene?", 1)
        pdf.ln()
        
        pdf.set_font("helvetica", "", 8)
        tradeoffs = [
            ("Hash Table", "Espacio (array grande, colisiones)", "Búsqueda/insertar en O(1) promedio vs O(n)"),
            ("B-Tree (Índices)", "Espacio en disco (estructura índice)", "Búsqueda O(log_B n) con mínimas lecturas vs scan"),
            ("Trie / Suffix", "Espacio (almacena todos prefijos)", "Búsqueda de patrones en O(m) sin escanear texto"),
            ("Skip List", "Espacio (niveles extra de punteros)", "Búsqueda O(log n) sin árboles auto-ajustables"),
            ("Bloom Filter", "Exactitud (falsos positivos)", "Espacio compacto + consulta O(k)"),
            ("Adjacency Matrix", "Espacio O(V^2)", "Consulta de arista en O(1) vs O(V) en lista"),
            ("Cache / Memoización", "RAM (almacena resultados previos)", "Evita recalcular: O(1) en vez de O(n) u O(2^n)")
        ]
        
        for t in tradeoffs:
            pdf.cell(40, 7, t[0], 1)
            pdf.cell(70, 7, t[1], 1)
            pdf.cell(80, 7, t[2], 1)
            pdf.ln()
            
        pdf.ln(8)
        
        # Conclusión del Trade-Off requerida
        pdf.set_font("helvetica", "B", 10)
        pdf.cell(0, 8, "Conclusión del Trade-Off del Sistema:", ln=True)
        pdf.set_font("helvetica", "", 10)
        pdf.multi_cell(190, 6, "Sacrificado: Espacio adicional en disco para almacenar el índice JSON en memoria/archivo y mantener tablas hash de mapeo directo.")
        pdf.multi_cell(190, 6, "Obteniendo: Acceso aleatorio inmediato O(1) mediante seek() sin necesidad de recorrer secuencialmente todo el archivo de contactos.")
        
        pdf.output(ruta)
        return ruta
