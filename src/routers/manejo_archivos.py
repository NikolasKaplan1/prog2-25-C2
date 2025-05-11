"""
Exportadores a CSV tomando datos directamente de SQLite.
Dependen de src.database.db_manager.get_connection().
"""
import pickle
import csv
from pathlib import Path
from datetime import date
from src.database.db_manager import get_connection
from src.models.inversor import Inversor
from src.models.transaccion import Transaccion

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

def exportar_transacciones_csv(transacciones: list[Transaccion], ruta: Path = DATA_DIR / "transacciones.csv"):
    """
    Exporta una lista de transacciones a un archivo CSV.

    Parameters
    ----------
    transacciones : list[Transaccion]
        Lista de objetos Transaccion a exportar.
    ruta : Path
        Ruta destino del archivo CSV.
    
    Raises
    ------
    ValueError
        Si la lista de transacciones está vacía.
    """
    if not transacciones:
        raise ValueError("La lista de transacciones está vacía. No se puede exportar. ")
    with ruta.open("w", newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(["inversor", "accion", "simbolo", "cantidad", "precio", "fecha"])
        for t in transacciones:
            writer.writerow([
                t["inversor"],
                t["accion"],
                t["simbolo"],
                t["cantidad"],
                t["precio"],
                t["fecha"].strftime("%Y-%m-%d %H:%M:%S")
            ])

def exportar_inversores_pickle(lista_inversores: list[Inversor], ruta: Path = DATA_DIR / "inversores.pkl"):
    """
    Exporta una lista de inversores a un archivo .pkl usando Pickle.

    Parameters
    ----------
    lista_inversores : list[Inversor]
        Lista de objetos Inversor.
    ruta : Path
        Ruta destino del archivo Pickle.
    """
    with ruta.open("wb") as f:
        pickle.dump(lista_inversores, f)


def importar_inversores_pickle(ruta: Path = DATA_DIR / "inversores.pkl") -> list[Inversor]:
    """
    Importa una lista de inversores desde un archivo Pickle.

    Parameters
    ----------
    ruta : Path
        Ruta del archivo .pkl a leer.

    Returns
    -------
    list[Inversor]
        Lista de objetos Inversor restaurados.

    Raises
    ------
    FileNotFoundError
        Si el archivo no fue encontrado.
    Exception
        Si ocurre un error si no se pudo importar el archivo.
    
    """
    try:
        with ruta.open("rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
    except Exception as e:
        raise Exception(f"No se pudo importar el archivo {ruta}: {e}")
