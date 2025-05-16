"""
Exportadores a CSV tomando datos directamente de SQLite.
Dependen de src.database.db_manager.get_connection().
"""
import pickle
import csv
import os
from pathlib import Path
from datetime import date
from src.database.db_manager import get_connection
from src.models.inversor import Inversor
from src.models.transaccion import Transaccion
from models.accion import Accion, AccionReal
from models.mercado import Mercado

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def asegurar_directorio(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
# ---------------------- CSV ----------------------

def exportar_acciones_csv(ruta: Path = DATA_DIR / "acciones.csv") -> None:
    with get_connection() as conn, ruta.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["simbolo", "nombre", "precio_actual"])
        for row in conn.execute("SELECT simbolo, nombre, precio_actual FROM acciones"):
            writer.writerow(row)


def exportar_historial_precios_csv(ruta: Path = DATA_DIR / "historial_precios.csv") -> None:
    with get_connection() as conn, ruta.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["simbolo", "fecha", "precio"])
        for row in conn.execute(
            "SELECT simbolo, fecha, precio FROM historial_precios ORDER BY fecha"
        ):
            writer.writerow(row)


def exportar_mercados_csv(ruta: Path = DATA_DIR / "mercados.csv") -> None:
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

def exportar_acciones_reales_csv(ruta: Path = DATA_DIR / 'acciones_reales.csv') -> None:
    """
    Exporta a un archivo CSV la lista de acciones reales registradas.

    Parameters
    ----------
    ruta : Path, optional
        Ruta de destino del archivo CSV. Por defecto es 'data/acciones_reales.csv'.

    Returns
    -------
    None
    """
    asegurar_directorio(ruta)
    with open(ruta, mode='w', newline='') as archivo:
        csv_writer = csv.writer(archivo)
        csv_writer.writerow(['simbolo', 'nombre', 'precio_actual'])
        for acc in AccionReal._acciones_reales_registradas.values():
            csv_writer.writerow([acc.simbolo, acc.nombre, acc._precio_actual])

def exportar_acciones_bancarrota_csv(ruta: Path = DATA_DIR / 'acciones_bancarrota.csv') -> None:
    """
    Exporta a un archivo CSV la lista de acciones en bancarrota registradas.

    Parameters
    ----------
    ruta : Path, optional
        Ruta de destino del archivo CSV. Por defecto es 'data/acciones_bancarrota.csv'.

    Returns
    -------
    None
    """
    asegurar_directorio(ruta)
    with open(ruta, mode='w', newline='') as archivo:
        csv_writer = csv.writer(archivo)
        csv_writer.writerow(['simbolo', 'nombre', 'fecha_bancarrota'])
        for acc in Accion._acciones_registradas.values():
            if acc._precio_actual == 0:
                fecha,_ = list(acc.historial_precios())[-1]
                csv_writer.writerow([acc.simbolo, acc.nombre, fecha])

def acciones_por_mercado_csv(ruta: Path = DATA_DIR / 'acciones_por_mercado.csv') -> None:
    """
    Exporta a un archivo CSV el número de acciones por mercado en los mercados registrados.

    Parameters
    ----------
    ruta : Path, optional
        Ruta de destino del archivo CSV. Por defecto es 'data/acciones_por_mercado.csv'.

    Returns
    -------
    None
    """
    asegurar_directorio(ruta)
    with open(ruta, mode='w', newline='') as archivo:
        csv_writer = csv.writer(archivo)
        csv_writer.writerow(['nombre_mercado', 'simbolo'])
        for nombre, mercado in Mercado._mercados_registrados.items():
            for acc in mercado._lista_acciones:
                csv_writer.writerow([nombre, acc.simbolo])

def exportar_transacciones_csv(transacciones: list[Transaccion], ruta: Path = DATA_DIR / "transacciones.csv") -> None:
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

# ---------------------- PICKLE ----------------------

def exportar_acciones_pickle(ruta: Path = DATA_DIR / 'acciones.pkl') -> None:
    """
    Exporta a un archivo Pickle los datos de las acciones registradas.

    Parameters
    ----------
    ruta : Path, optional
        Ruta de destino del archivo CSV. Por defecto es 'data/acciones.pkl'.

    Returns
    -------
    None
    """
    asegurar_directorio(ruta)
    with open(ruta, 'wb') as f:
        pickle.dump(Accion._acciones_registradas, f)

def importar_acciones_pickle(ruta: Path = DATA_DIR / 'acciones.pkl') -> dict[str, Accion]:
    """
    Importa los datos de acciones registradas desde un archivo Pickle.

    Parameters
    ----------
    ruta : Path, optional
        Ruta del archivo Pickle. Por defecto es 'data/acciones.pkl'.

    Returns
    -------
    dict[str, Accion]
        Diccionario con los objetos Accion restaurados, indexados por símbolo.

    Raises
    ------
    FileNotFoundError
        Si el archivo no existe.
    Exception
        Si ocurre un error durante la deserialización.
    """
    try:
        with ruta.open('rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
    except Exception as e:
        raise Exception(f"No se pudieron importar las acciones desde {ruta}: {e}")


def exportar_historiales_pickle(ruta: Path = DATA_DIR / 'historiales.pkl') -> None:
    """
    Exporta a un archivo Pickle el historial de precios de las acciones registradas.

    Parameters
    ----------
    ruta : Path, optional
        Ruta de destino del archivo CSV. Por defecto es 'data/historiales.pkl'.

    Returns
    -------
    None
    """
    asegurar_directorio(ruta)
    historiales = {simbolo: acc.historial_precios for simbolo, acc in Accion._acciones_registradas.items()}
    with open(ruta, 'wb') as f:
        pickle.dump(historiales, f)

def importar_historiales_pickle(ruta: Path = DATA_DIR / 'historiales.pkl') -> dict[str, list[float]]:
    """
    Importa el historial de precios de las acciones desde un archivo Pickle.

    Parameters
    ----------
    ruta : Path, optional
        Ruta del archivo Pickle. Por defecto es 'data/historiales.pkl'.

    Returns
    -------
    dict[str, list[float]]
        Diccionario con los historiales de precios por símbolo.

    Raises
    ------
    FileNotFoundError
        Si el archivo no existe.
    Exception
        Si ocurre un error durante la deserialización.
    """
    try:
        with ruta.open('rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
    except Exception as e:
        raise Exception(f"No se pudieron importar los historiales desde {ruta}: {e}")

def exportar_mercados_registrados_pickle(ruta: Path = DATA_DIR / 'mercados_registrados.pkl') -> None:
    """
    Exporta a un archivo Pickle los datos de los mercados registrados.

    Parameters
    ----------
    ruta : Path, optional
        Ruta de destino del archivo CSV. Por defecto es 'data/mercados_registrados.pkl'.

    Returns
    -------
    None
    """
    asegurar_directorio(ruta)
    with open(ruta, 'wb') as f:
        pickle.dump(Mercado._mercados_registrados, f)

def importar_mercados_registrados_pickle(ruta: Path = DATA_DIR / 'mercados_registrados.pkl') -> dict[str, Mercado]:
    """
    Importa los datos de los mercados registrados desde un archivo Pickle.

    Parameters
    ----------
    ruta : Path, optional
        Ruta del archivo Pickle. Por defecto es 'data/mercados_registrados.pkl'.

    Returns
    -------
    dict[str, Mercado]
        Diccionario con los objetos Mercado restaurados, indexados por nombre o clave.

    Raises
    ------
    FileNotFoundError
        Si el archivo no existe.
    Exception
        Si ocurre un error durante la deserialización.
    """
    try:
        with ruta.open('rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
    except Exception as e:
        raise Exception(f"No se pudieron importar los mercados desde {ruta}: {e}")

def exportar_inversores_pickle(lista_inversores: list[Inversor], ruta: Path = DATA_DIR / "inversores.pkl") -> None:
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

