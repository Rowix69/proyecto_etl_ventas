import csv
import json
from datetime import datetime
from collections import defaultdict

# LEER LOS DATOS
def extraer_ventas(ruta_csv):
    "Lee el csv y devuelve una lista de diccionarios"
    with open(ruta_csv, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# TRANSFORMAR LOS DATOS
def transformar_ventas(ventas_raw):
    "Limpia los datos sucios y calcula el total"
    limpias = []
    errores = []
    for i, venta in enumerate(ventas_raw):
        try:
            if not venta.get("producto", "").strip():
                raise ValueError("Producto vacío")

            # LIMPIAR Y VALIDAR LA CANTIDAD
            cantidad_raw = venta.get("cantidad", "").strip()
            cantidad = int(cantidad_raw) if cantidad_raw else 1

            # LIMPIAR Y VALIDAR EL PRECIO
            precio_raw = venta.get("precio_unitario", "").strip()
            precio = float(precio_raw) if precio_raw and precio_raw != "N/A" else 0.0

            # CALCULAR EL TOTAL
            total = cantidad * precio

            # AGREGAR LA VENTA LIMPIA A LA LISTA
            limpias.append({
                "fecha": venta["fecha"],
                "producto": venta["producto"],
                "categoria": venta["categoria"],
                "cantidad": cantidad,
                "precio_unitario": precio,
                "total": round(total, 2),
                "cliente": venta["cliente"]
            })
        except (ValueError, TypeError) as e:
            errores.append({
                "fila": i + 2,
                "error": str(e),
                "datos": dict(venta)
            })
    return limpias, errores

# ANALIZAR LOS DATOS

def generar_resumen(ventas_limpias):
    "Genera un resumen en base a los datos limpios"
    if not ventas_limpias:
        return {"error": "No hay datos validos"}

    total_facturado = sum(v["total"] for v in ventas_limpias)
    num_transacciones = len(ventas_limpias)
    ticket_medio = total_facturado / num_transacciones if num_transacciones else 0

    por_categoria = defaultdict(lambda: {"total": 0, "transacciones": 0})
    for venta in ventas_limpias:
        cat = venta["categoria"]
        por_categoria[cat]["total"] += venta["total"]
        por_categoria[cat]["transacciones"] += 1

    productos_total = defaultdict(float)
    for venta in ventas_limpias:
        productos_total[venta["producto"]] += venta["total"]

    top_productos = sorted(productos_total.items(), key=lambda x: x[1], reverse=True)[:3]

    clientes_unicos = set(v["cliente"] for v in ventas_limpias)

    return {
        "fecha_reporte": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "total_facturado": round(total_facturado, 2),
        "num_transacciones": num_transacciones,
        "ticket_medio": round(ticket_medio, 2),
        "clientes_unicos": list(clientes_unicos),
        "por_categoria": dict(por_categoria),
        "top_3_productos": [
            {"producto": prod, "total": round(total, 2)} for prod, total in top_productos
        ]
    }


# ESCRIBIR LOS RESULTADOS

def guardar_resultado(resumen, errores, ruta_salida, ruta_errores):
    "Guarda el resumen y los errores en archivos JSON"
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)

    with open(ruta_errores, 'w', encoding='utf-8') as f:
        json.dump(errores, f, ensure_ascii=False, indent=2)


# FUNCION PRINCIPAL
def main():
    "Entrada del pipeline de ventas"

    print("*"*50)
    print("Pipeline de Ventas - Procesamiento de Datos")
    print("*"*50)

    # CONFIGURACIÓN DE RUTAS
    ruta_csv = "data/ventas.csv"
    ruta_salida = "data/resumen_ventas.json"
    ruta_errores = "data/errores_ventas.json"

    # EXTRACCION
    print("Extrayendo datos...")
    ventas_raw = extraer_ventas(ruta_csv)
    print(f"Leidos {len(ventas_raw)} registros de ventas.")

    # TRANSFORMACION
    print("Transformando datos...")
    ventas_limpias, errores = transformar_ventas(ventas_raw)
    tasa_exito = len(ventas_limpias) / len(ventas_raw) * 100 if ventas_raw else 0
    print(f"Validos: {len(ventas_limpias)} ({tasa_exito:.2f}%) ")
    print(f"Errores: {len(errores)}")

    # ANALISIS
    print("Generando resumen...")
    resumen = generar_resumen(ventas_limpias)
    print(f"Total facturado: {resumen.get('total_facturado', 0)}")

    # GUARDAR RESULTADOS
    print("Guardando resultados...")
    guardar_resultado(resumen, errores, ruta_salida, ruta_errores)
    print(f"Resumen guardado en '{ruta_salida}'")
    if errores:
        print(f"Se encontraron {len(errores)} errores. Detalles en '{ruta_errores}'.")

    # REPORTE FINAL
    print("\n"+"="*50)
    print("RESUMEN")
    print("="*50)
    print(f"Facturado total: {resumen.get('total_facturado', 0)}")
    print(f"Ticket medio: {resumen.get('ticket_medio', 0)}")
    print(f"Transacciones: {resumen.get('num_transacciones', 0)}")
    print(f"Clientes únicos: {len(resumen.get('clientes_unicos', []))}")
    print(f"\n Top 3 productos por facturación:")
    for item in resumen.get("top_3_productos", []):
        print(f" - {item['producto']}: {item['total']}")
    print("="*50)

if __name__ == "__main__":
    main()