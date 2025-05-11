"""
Exportadores a CSV tomando datos directamente de SQLite.
Dependen de src.database.db_manager.get_connection().
"""

import csv
from pathlib import Path
from datetime import date
from src.database.db_manager import get_connection

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def exportar_acciones_csv(ruta: Path = DATA_DIR / "acciones.csv"):
    with get_connection() as conn, ruta.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["simbolo", "nombre", "precio_actual"])
        for row in conn.execute("SELECT simbolo, nombre, precio_actual FROM acciones"):
            writer.writerow(row)


def exportar_historial_precios_csv(ruta: Path = DATA_DIR / "historial_precios.csv"):
    with get_connection() as conn, ruta.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["simbolo", "fecha", "precio"])
        for row in conn.execute(
            "SELECT simbolo, fecha, precio FROM historial_precios ORDER BY fecha"
        ):
            writer.writerow(row)


def exportar_mercados_csv(ruta: Path = DATA_DIR / "mercados.csv"):
    with get_connection() as conn, ruta.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["nombre_mercado", "numero_acciones", "fecha_export"])
        for nombre, count in conn.execute(
            """SELECT m.nombre, COUNT(a.simbolo)
                 FROM mercados m
                 LEFT JOIN acciones a ON a.mercado_id = m.id
                 GROUP BY m.id"""
        ):
            writer.writerow([nombre, count, date.today()])
