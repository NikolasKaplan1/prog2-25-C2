from models import Inversor, Accion
from inversor_agresivo import InversorAgresivo
import pandas as pd

class IA():
    def __init__(self,inversor: Inversor):
        self.inversor = inversor
    def recomendacion(self):
        capital = self.inversor.capital
        cartera = self.inversor.cartera
        acciones_registradas = Accion.acciones_registradas
        acciones = []
        for accion in acciones_registradas:
            #vamos añadiendo acciones al diccionario acciones en el que las claves sean los símbolos
            #y sus valores los precios actuales
            acciones.append({"Simbolo": accion, "Precio": acciones_registradas[accion].precio_actual})
        df_acciones = pd.DataFrame(acciones).sort_values(by='Precio', ascending = True) #creamos un dataframe con las acciones ordenados por su precio
        if capital <= df_acciones.iloc[0]["Precio"]:
            #si el capital es más pequeño que la acción más barata, no se puede comprar
            raise ValueError(f"No tienes suficiente dinero para comprar ninguna acción. Tu capital es de {capital} euros y la más barata vale {df.iloc[0]["Precio"]}")
        n = 0
        recomendaciones = {}
        #Al inversor agresivo le recomienda las acciones más caras y al conservador las más baratas
        recomendaciones_nuevas = {}
        #Este hace lo mismo que el anterior solo que únicamente recomienda las acciones que no están en la cartera del inversor
        if isinstance(inversor,InversorAgresivo):
            df_acciones = df_acciones.sort_values(by='Precio', ascending = False)
            for _, row in df_acciones.iterrows():
                if row["Precio"] <= capital:
                    recomendaciones[row["Simbolo"]] = row["Precio"]
                    n += 1
                if n == 5:
                    break
            n = 0
            for _, row in df_acciones.iterrows():
                if row["Precio"] <= capital and (row["Simbolo"] not in cartera):
                    recomendaciones_nuevas[row["Simbolo"]] = row["Precio"]
                    n += 1
                if n == 5:
                    break
        else:
            for _, row in df_acciones.iterrows():
                if row["Precio"] > capital:
                    break
                recomendaciones[row["Simbolo"]] = row["Precio"]
                n += 1
                if n == 5:
                    break
            n = 0
            for _, row in df_acciones.iterrows():
                if row["Precio"] > capital:
                    break
                if row["Simbolo"] not in cartera:
                    recomendaciones_nuevas[row["Simbolo"]] = row["Precio"]
                    n += 1
                if n == 5:
                    break
        return recomendaciones, recomendaciones_nuevas

            