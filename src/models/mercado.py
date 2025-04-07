import random
from accion import Accion
from typing import Union

class Mercado:
    """Esta clase simulará un mercado financiero con un listado de acciones

    Atributos
    -------------
    lista_acciones: list[Accion]
        Una lista de las acciones que hay en el mercado
    
    Métodos
    -------------
    registrar_accion(accion: Accion)
        Sirve para añadir una acción al mercado
    obtener_precio(simbolo: str) -> float
        Te da el precio de una acción dado su símbolo
    bancarrota(simbolo: str)
        Declara en bancarrota una acción dado su símbolo.
    simular_movimientos()
        Simula movimientos de un mercado (cambia precios aleatoriamente)

    """
    def __init__(self, lista_acciones: list[Accion]):
        """
        Parámetros
        -------------
        lista_acciones: list[Accion]
            Es una lista en la que se encuentran todas las acciones disponibles en el mercado
        
        Raises
        -------------
        TypeError
            En el caso de que algún objeto de lista_acciones no sea una acción, salta error.
        """
        
        for accion in lista_acciones:
            if type(accion) is not Accion:
                raise TypeError(f"El objeto {accion} no pertenece a la clase Accion")
        self.lista_acciones = lista_acciones

    def registrar_accion(self, accion: Accion):
        """Este método sirve para registrar una nueva acción en el mercado
        
        Parámetros
        -------------
        accion: Accion
            La acción que queremos registrar

        Raises
        -------------
        TypeError
            En el caso de que acción no sea de Acción, salta error.
        """

        if type(accion) is not Accion:
            raise TypeError(f'El objeto {accion} no pertenece a la clase Accion')
        self.lista_acciones.append(accion)
        
    def obtener_precio(self,simbolo: str) -> Union[float,str]:
        """Este método sirve para obtener el precio de una acción dado su símbolo

        Parámetros
        -------------
        simbolo: str
            El símbolo de la acción de la que queremos obtener su precio
        """
        for accion in self.lista_acciones:
            if accion.simbolo == simbolo:
                return accion.precio_actual
        return "No existen acciones con este símbolo"

    def bancarrota(self,simbolo: str):
        """Este método sirve para declarar en bancarrota una acción dado su símbolo. Lo que
        hace es eliminarla de lista_acciones y actualiza su precio a 0.
    
        Parámetros
        -------------
        simbolo: str
            El símbolo de la acción que queremos declarar en bancarrota.
        """
        for accion in lista_acciones:
            if accion.simbolo == simbolo:
                lista_acciones.remove(accion)
                accion.actualizar_precio(0)
                break
        
    def simular_movimientos(self):
        """Este método sirve para simular movimientos en el mercado (cambia de precio
        aleatoriamente todas las acciones.)
        """
        for accion in self.lista_acciones:
            variacion = random.uniform(-0.3, 0.3)
            nuevo_precio = round(accion.precio_actual * (1 + variacion), 3)
            accion.actualizar_precio(nuevo_precio)

