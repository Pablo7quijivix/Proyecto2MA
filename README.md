# Proyecto2MA

Sistema de Gestión de Agenda de Contactos - Acceso Aleatorio y Estructura de Longitud FijaDescripción GeneralEl sistema es una aplicación de escritorio desarrollada en Python bajo una arquitectura modular estricta. Su propósito principal es la administración eficiente de registros de contactos mediante una estructura de almacenamiento binario de tamaño fijo, acceso aleatorio directo en tiempo constante $O(1)$ apoyado por una tabla hash en memoria y un índice primario JSON, control criptográfico de integridad, compresión de respaldos y una interfaz gráfica interactiva.Estructura y Arquitectura del ProyectoEl proyecto se organiza de manera modular para separar la lógica de negocio, la persistencia, la interfaz de usuario y las utilidades de exportación:proyecto_agenda/
│
├── main.py                          <-- Archivo principal de ejecución
├── core/                            <-- Lógica de negocio y gestión del sistema
│   ├── __init__.py
│   ├── contact_manager.py           <-- Manejo de registros (100 bytes), acceso aleatorio, CRUD y SHA-256
│   ├── index_manager.py             <-- Gestión de tabla hash en memoria y persistencia del índice en JSON
│   └── exporter.py                  <-- Generación de reportes PDF de eficiencia y exportación JSON
├── carga_de_datos/                  <-- Módulo de importación y carga masiva
│   ├── __init__.py
│   └── cargar_datos_propuestos.py   <-- Lógica de lectura, parseo y conversión de archivos externos (.txt, .csv)
├── ui/                              <-- Interfaz gráfica de usuario
│   ├── __init__.py
│   └── main_window.py               <-- Ventana principal (Tkinter), pestañas, formularios, botones y visor tabular
├── archivos_generados/              <-- Directorio de persistencia operativa del sistema
│   ├── DAT/
│   │   └── contactos.dat            <-- Archivo binario de registros de tamaño fijo
│   ├── JSON/
│   │   └── indice.json              <-- Archivo del índice primario
│   ├── SHA256/
│   │   └── contactos.sha256         <-- Hash de control de integridad criptográfica
│   ├── PDF/                         <-- Reportes exportados
│   └── ZIP/
│       └── respaldo_agenda.zip      <-- Respaldo comprimido del sistema
└── Eficiencia/                      <-- Documentación y métricas
    └── reporte_eficiencia.pdf       <-- Reporte técnico de complejidad temporal y análisis Trade-Off
Aspectos Técnicos y Teóricos
1. Estructura de Registros de Tamaño FijoEl almacenamiento principal se realiza en el archivo binario archivos_generados/DAT/contactos.dat. Cada registro posee una longitud estrictamente constante de 100 bytes, distribuida de la siguiente manera:ID: 5 bytes (Identificador numérico único).Nombre: 30 bytes (Nombre completo del contacto).Teléfono: 15 bytes (Número telefónico de carácter exclusivamente numérico).Correo: 30 bytes (Dirección de correo electrónico).Ciudad: 20 bytes (Ubicación geográfica o ciudad).Los campos son formateados mediante normalización de texto y ajuste de relleno (ljust) para garantizar que la suma total sea constante, permitiendo el cálculo matemático exacto de las posiciones en disco.
   
2. Acceso Aleatorio mediante seek() y tell()
Gracias a la constancia de los 100 bytes por registro, el sistema evita recorridos secuenciales costosos. Cuando se requiere buscar, modificar o eliminar un registro, el índice primario suministra el número de registro exacto (num_reg). Mediante la instrucción seek(num_reg * TAMANO_REGISTRO), el puntero del archivo binario se desplaza de manera directa e inmediata a la posición del contacto, logrando una eficiencia de tiempo promedio de orden $O(1)$.
   
3. Índice Primario y Tabla Hash (JSON)
El módulo IndexManager mantiene una estructura de diccionario en memoria que actúa como una Tabla Hash, enlazando cada ID único con su respectivo número de registro. Esta estructura se persiste automáticamente en el archivo archivos_generados/JSON/indice.json.Eficiencia frente a búsqueda secuencial: Mientras que una búsqueda lineal o secuencial requiere recorrer el archivo bloque por bloque evaluando una complejidad temporal de $O(N)$, el uso del índice primario reduce la búsqueda a una operación directa de recuperación en la tabla hash, optimizando drásticamente el rendimiento operativo.

4. Control de Integridad SHA-256
Para garantizar que los datos no hayan sido alterados externamente (por manipulación manual de archivos), el sistema calcula un resumen criptográfico SHA-256 del archivo binario contactos.dat cada vez que este es modificado, almacenando el resultado en archivos_generados/SHA256/contactos.sha256. Al inicializarse la aplicación, se recalcula y contrasta el hash actual, emitiendo una advertencia de seguridad en caso de detectarse discrepancias o corrupción.


5. Compresión de Respaldos (ZIP)
La herramienta de respaldo integra el algoritmo de compresión DEFLATED mediante bibliotecas estándar, generando un archivo comprimido archivos_generados/ZIP/respaldo_agenda.zip que agrupa el archivo de datos y el índice. Esto permite optimizar el almacenamiento físico en disco comparado con el peso acumulado de los archivos originales.

Requisitos de Ejecución
Entorno de ejecución de Python 3.10 o superior.Librerías estándar integradas en Python (os, hashlib, zipfile, json, unicodedata, tkinter). No requiere la instalación de dependencias externas adicionales de terceros.

Instrucciones de Ejecución
Clonar o ubicar la carpeta raíz del proyecto en el equipo local.
Abrir una terminal en el directorio principal.
Ejecutar el script principal mediante el comando:python main.py
Interactuar con la interfaz gráfica para realizar operaciones de creación, búsqueda, modificación, eliminación, carga masiva desde archivos .csv/.txt, exportación y verificación de integridad.
