import random
from accion import Accion
from typing import Union

class Mercado:
    """Esta clase simulará un mercado financiero con un listado de acciones

    Atributos
    -------------
    nombre: str
        Nombre del mercado
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
    mercados_registrados: dict[str,Mercado] = {}
    def __init__(self, nombre: str, lista_acciones: list[Accion]):
        """
        Parámetros
        -------------
        nombre: str
            Nombre del mercado
        lista_acciones: list[Accion]
            Es una lista en la que se encuentran todas las acciones disponibles en el mercado
        
        Raises
        -------------
        ValueError
            En el caso de que ya existe un mercado con el nombre que pasamos
        ValueError
            No puede haber acciones repetidas en lista_acciones
        TypeError
            En el caso de que algún objeto de lista_acciones no sea una acción, salta error.
        """
        if nombre in mercados_registrados:
            raise ValueError(f"Ya existe un mercado con el nombre {nombre}")
        for i in range(len(lista_acciones)):
            accion = lista_acciones[i]
            if accion in lista[:i]:
                raise ValueError(f"No puede haber acciones repetidas")
            if not isinstance(accion,Accion):
                raise TypeError(f"El objeto {accion}, que es el término {i}, no pertenece a la clase Accion")
        
        self.nombre = nombre
        self.lista_acciones = lista_acciones
        Mercado.mercados_registrados[nombre] = self

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

        if not isinstance(accion,Accion):
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

