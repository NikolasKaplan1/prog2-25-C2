
class Mercado:
    """
    La clase Mercado indica la lista de acciones que se encuentran ahora mismo disponibles. Además, 
    permite registrar nuevas accioens y obtener el precio de las ya existentes.

    Métodos
    -------------
    registrar_accion(accion)
        Permite añadir una nueva acción a la lista de acciones actual.

    obtener_precio(simbolo)
        Dado el símbolo de la acción, te su precio

    simular_movimientos

    """
    def __init__(self, lista_acciones: list[Accion]):
        """
        Parámetros
        -------------
        lista_acciones: list[Accion]
        Consiste en una lista en la que están todas las acciones que hay actualmente en el mercado.
        """
        self.lista_acciones = lista_acciones
    def registrar_accion(self, accion: Accion):
        """Registra una accion si esta no está ya en la lista de acciones
        Parámetros
        -------------
        accion: Accion
            Es la acción que quieres registrar
        """
        if accion not in self.lista_acciones:
            self.lista_acciones.append(accion)
        else:
            print("Esta acción ya está en la lista de acciones")
    def obtener_precio(self,simbolo: str) -> float:
        """Te devuelve el precio de la acción que solicitas en formato float
        Parámetros
        -------------
        simbolo: str
            El simbolo de la accion de la que quieres saber su precio
        """
        for accion in self.lista_acciones:
            if accion.simbolo == simbolo:
                return accion.precio_actual
        print("No existe ninguna acción con ese símbolo")
    def simular_movimientos():
        pass
