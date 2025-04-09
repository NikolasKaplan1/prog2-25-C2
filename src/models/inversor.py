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

    
    Atributos
    -------------

    nombre : str
        Nombre del inversor.
    
    capital : float
        Dinero disponible en su cuenta
    
    cartera : dict
        Acciones en posesión del inversor
    
    
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
    def __init__(self, nombre:str, capital:float, cartera: dict[Accion, float]):
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
        """ Compra acciones si tiene suficiente capital"""
        costo_total = accion.precio * cantidad
        if self.capital >= costo_total:
            self.capital -= costo_total
            self.cartera[accion.simbolo] -= self.cartera.get(accion.simbolo, 0) + cantidad
            self.registrar_transaccion("Compra", accion.simbolo, cantidad, accion.precio)
        else:
            print ("Fondos insuficientes")


    def vender(self, accion:Accion, cantidad:int):
        """ Vende acciones si las tiene disponibles"""
        if self.cartera.get(accion.simbolo, 0) >= cantidad:
            self.capital += accion.precio * cantidad
            self.cartera[accion.simbolo] -= cantidad
            self.registrar_transaccion("Venta", accion.simbolo, cantidad, accion.precio)
        else:
            print("No tienes suficientes acciones para vender")
    
    def mostrar_cartera(self):
        """ Devuelve la cartera actual del inversor"""
        return self.cartera

    def __str__(self):
         return f"Inversor {self.nombre} - Capital: {self.capital} - Cartera: {self.cartera}"


    def __add__(self, other):
        """ Permite sumar el capital entre inversores"""
        if isinstance(other, Inversor):
            return Inversor(self.nombre + " & " + other.nombre, self.capital + other.capital)
        pass
        

class InversorAgresivo(Inversor):
    pass

