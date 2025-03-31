"""
class Inversor:
    def __init__(self, nombre: str, capital: float, cartera: dict[Accion, float]):
        self.nombre = nombre
        self.capital = capital
        self.cartera = cartera
    def comprar(self, accion: Accion, cantidad: float):
        if accion not in self.cartera:
            self.cartera[accion] = cantidad
        else:
            self.cartera[accion] += cantidad
    def vender(self, accion: Accion, cantidad: float):
        if accion not in self.cartera:
            print(f"No puedes vender {accion} porque no tienes ese tipo de acción.")
        elif self.cartera[accion] < cantidad:
            print(f"No tienes tantas acciones de {accion}")
        else:
            self.cartera[accion] -= cantidad

    def __str__(self):
        return f"La cartera de {self.nombre} tiene un capital de {self.capital}" + \
            + f"y contiene las siguientes acciones: {self.cartera}"

"""

from accion import Accion


class Inversor:
    """
    La clase Inversor representa a un persona que invierte en el mercado funanciero. Además le 
    permite gestionar su capital a la cartera de acciones.

    Métodos
    -------------
    comprar(accion, cantidad)
        Verifica si es posible hacer una compra y le descuenta el coste. Añade las acciones a la cartera
        y registra la transacción.


    vender(accion, cantidad)
        Verifica si hay suficientes acciones y las vende. Añade el dinero de la venta y registra
        la transacción.

    mostrar_cartera()
        Devuelve un diccionario con las acciones y la cantidad que tiene.

    __str__():
        Devuelve una lista con todas las transacciones en formato texto.

    """
    def __init__(self, nombre:str, capital:float):
        """
        Parámetros
        ---------------
        nombre
            Nombre del inversor.

        capital
            Cantidad de dinero que tiene el inversor en su cuenta.

        cartera
            Diccionario donde la claves son símbolos y los valores las cantidades de acciones que poseen.

        """
        self.nombre = nombre
        self.capital = capital
        self.cartera = {}


    def comprar(self, accion:Accion, cantidad:int):
        pass

    def vender(self, accion:Accion, cantidad:int):
        pass

    def mostrar_cartera(self):
        pass

    def __str__(self):
        pass