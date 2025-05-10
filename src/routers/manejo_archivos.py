import csv
import pickle
import os
from datetime import date

from models.accion import Accion
from models.mercado import Mercado

# Asegura que el directorio existe
def asegurar_directorio(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)

# ---------------------- CSV ----------------------

def exportar_acciones_csv(ruta='data/acciones.csv'):
    asegurar_directorio(ruta)
    with open(ruta, mode='w', newline='') as archivo:
        csv_writer = csv.writer(archivo)
        csv_writer.writerow(['simbolo', 'nombre', 'precio_actual'])
        for acc in Accion.acciones_registradas.values():
            csv_writer.writerow([acc.simbolo, acc.nombre, acc.precio_actual])

def exportar_acciones_reales_csv(ruta='data/acciones_reales.csv'):
    asegurar_directorio(ruta)
    with open(ruta, mode='w', newline='') as archivo:
        csv_writer = csv.writer(archivo)
        csv_writer.writerow(['simbolo', 'nombre', 'precio_actual'])
        for acc in AccionReal.acciones_reales_registradas.values():
            csv_writer.writerow([acc.simbolo, acc.nombre, acc.precio_actual])

def exportar_historial_precios_csv(ruta='data/historial_precios.csv'):
    asegurar_directorio(ruta)
    with open(ruta, mode='w', newline='') as archivo:
        csv_writer = csv.writer(archivo)
        csv_writer.writerow(['simbolo', 'fecha', 'precio'])
        for acc in Accion.acciones_registradas.values():
            for fecha, precio in acc.historial_precios.items():
                csv_writer.writerow([acc.simbolo, fecha, precio])

def exportar_acciones_bancarrota_csv(ruta='data/acciones_bancarrota.csv'):
    asegurar_directorio(ruta)
    with open(ruta, mode='w', newline='') as archivo:
        csv_writer = csv.writer(archivo)
        csv_writer.writerow(['simbolo', 'nombre', 'fecha_bancarrota'])
        for acc in Accion.acciones_registradas.values():
            if acc.precio_actual == 0:
                fecha,_ = list(acc.historial_precios())[-1]
                csv_writer.writerow([acc.simbolo, acc.nombre, fecha])

def exportar_mercados_csv(ruta='data/mercados.csv'):
    asegurar_directorio(ruta)
    with open(ruta, mode='w', newline='') as archivo:
        csv_writer = csv.writer(archivo)
        csv_writer.writerow(['nombre_mercado', 'numero_acciones', 'fecha_creacion'])
        for nombre, mercado in Mercado.mercados_registrados.items():
            csv_writer.writerow([nombre, len(mercado.lista_acciones), date.today()])

def acciones_por_mercado_csv(ruta='data/acciones_por_mercado.csv'):
    asegurar_directorio(ruta)
    with open(ruta, mode='w', newline='') as archivo:
        csv_writer = csv.writer(archivo)
        csv_writer.writerow(['nombre_mercado', 'simbolo'])
        for nombre, mercado in Mercado.mercados_registrados.items():
            for acc in mercado.lista_acciones:
                csv_writer.writerow([nombre, acc.simbolo])

# ---------------------- PICKLE ----------------------

def exportar_acciones_pickle(ruta='data/acciones.pkl'):
    asegurar_directorio(ruta)
    with open(ruta, 'wb') as f:
        pickle.dump(Accion.acciones_registradas, f)

def exportar_historiales_pickle(ruta='data/historiales.pkl'):
    asegurar_directorio(ruta)
    historiales = {simbolo: acc.historial_precios for simbolo, acc in Accion.acciones_registradas.items()}
    with open(ruta, 'wb') as f:
        pickle.dump(historiales, f)


def exportar_mercados_registrados_pickle(ruta='data/mercados_registrados.pkl'):
    asegurar_directorio(ruta)
    with open(ruta, 'wb') as f:
        pickle.dump(Mercado.mercados_registrados, f)

