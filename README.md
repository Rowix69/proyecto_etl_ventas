# 📊 Pipeline ETL: Procesamiento de Ventas Diarias

Este es un proyecto de Ingeniería de Datos (ETL) construido en Python puro. Simula el procesamiento diario de transacciones de una tienda online, tomando datos "sucios", limpiándolos y generando un resumen ejecutivo automático.

## 🚀 Características del Proyecto
* **Extract (Extracción):** Lectura de datos desde archivos CSV.
* **Transform (Transformación):** Limpieza de datos, validación de tipos y manejo de excepciones (`try/except`) para tolerar filas corruptas sin detener la ejecución.
* **Load (Carga):** Agrupación de métricas (uso de `defaultdict`) y exportación de reportes a formato JSON.
* **Tolerancia a fallos:** Los registros con errores se aíslan y se guardan en un archivo `errores_dia.json` para auditoría.

## 🛠️ Tecnologías Usadas
* Python 3
* Librerías estándar: `csv`, `json`, `collections`, `datetime`, `os`
* Entorno virtual (`venv`)

## 📂 Estructura del Proyecto
```text
proyecto_etl_ventas/
│
├── data/                   # Carpeta de entrada/salida de datos
│   ├── ventas.csv          # Datos crudos (generados por el script)
│   ├── resumen_ventas.json # Salida: Reporte analítico limpio
│   └── errores_ventas.json # Salida: Log de registros corruptos
│
├── generar_datos.py        # Script generador de datos de prueba (Mock)
├── pipeline_ventas.py      # Motor principal ETL
├── .gitignore              # Archivos ignorados por Git
└── README.md               # Documentación del proyecto