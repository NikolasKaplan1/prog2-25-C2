from models import Inversor, Accion
from inversor_agresivo import InversorAgresivo
import pandas as pd

class IA():
    """
    Clase IA encargada de recomendar inversiones para un inversor, basándose en su tipo (Agresivo/Pasivo), su capital disponible y las acciones existentes.

    Atributos
    ------------
    inversor: Inversor
        Inversor que solicta recomendación.
    
    Métodos
    ------------
    recomendacion()
        Devuelve dos diccionarios con recomendaciones:
        - Uno con las mejores opciones según el tipo de inversor.
        - Otro que filtra posibles acciones nuevas que no tiene previamente.
    """
    def __init__(self,inversor: Inversor):
        """
        Constructor que inicializa la IA.

        Parámetros
        ------------
        inversor: Inversor 
            Objeto que representa al inversor (puede ser pasivo o agresivo).
        """
        self.inversor = inversor
    
    def recomendacion(self):
        """
        Genera recomendaciones de acciones que el inversor podría adquirir, siempre dependiendo de que:

        - Su tipo --> (Agresivo: prefiere acciones caras, ganancia rápida / Pasivo: prefiera acciones baratas, ganacia prolongada).
        - Su capital disponible --> ya que de no tener, no podrá adquirir.
        - Las acciones que ya posee --> no se le recomendaran acciones repetidas si ya pertenece a su cartera.
        
        Returns
        ----------
        tuple[dict, dict]
            - Primer diccionario: Recomendaciones generales para cada tipo (hasta 5).
            - Segundo diccionario: Solo nuevas acciones que no tiene el inversor.

        Raises:
        ---------------
        ValueError 
            Si no tienes suficiente dinero para comprar ninguna acción
        """
        
        # Datos necesarios
        capital = self.inversor.capital
        cartera = self.inversor.cartera
        acciones_registradas = Accion.acciones_registradas
        acciones = []
        
        for accion in acciones_registradas:
            # vamos añadiendo acciones al diccionario acciones en el que las claves sean los símbolos
            # y sus valores los precios actuales
            acciones.append({"Simbolo": accion, "Precio": acciones_registradas[accion].precio_actual})
        
        # Creamos un dataframe con las acciones ordenados por su precio
        df_acciones = pd.DataFrame(acciones).sort_values(by='Precio', ascending = True) 
        
        if capital <= df_acciones.iloc[0]["Precio"]:
            # Si el capital es menor que la acción más barata, no se podrá comprarla.
            raise ValueError(f"No tienes suficiente dinero para comprar ninguna acción. Tu capital es de {capital} euros y la más barata vale {df_acciones.iloc[0]["Precio"]}")
        
        n = 0
        recomendaciones = {}
        #Al inversor agresivo le recomienda las acciones más caras y al conservador las más baratas
        recomendaciones_nuevas = {}
        
        # Este hace lo mismo que el anterior solo que únicamente recomienda las acciones que no están en la cartera del inversor
        if isinstance(self.inversor,InversorAgresivo):
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
        # Si no es agresivo, se asume pasivo. Por lo que prefiere acciones más económicas.
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

            