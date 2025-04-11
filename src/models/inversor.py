from .accion import Accion
from typing import List


class Inversor:
    """
    La clase Inversor representa a una persona que invierte en el mercado financiero.
    Permite gestionar su capital y su cartera de acciones.

    Atributos
    ------------
    nombre: str
        Nombre del inversor
    capital: float
        Capital del inversor
    cartera: dict[str, Accion]
        Diccionario donde las claves son los símbolos de las acciones y los valores son instancias de Accion
    transacciones: list
        Lista de las transacciones realizadas
    
    Métodos
    ------------
    comprar(accion: Accion, cantidad: int)
        compras una cantidad de acciones
    vender(accion: Accion, cantidad: int)
        vendes una cantidad de acciones
    mostrar_cartera():
        te enseña la cartera del inversor
    registrar_transaccion(tipo, accion, cantidad)
        registrar una transaccion efectuada
    __add__(other: tuple[Accion,int])
        otro método para comprar una cantidad de acciones
    __sub__(other: tuple[Accion, int])
        otro método para vender una cantidad de acciones
    """


    def __init__(self, nombre: str, capital: float):
        """
        Inicializa un inversor con nombre y capital inicial.
        
        Parámetros:
        ------------
        - nombre: Nombre del inversor
        - capital: Capital inicial del inversor
        """
        self.nombre = nombre
        self.capital = capital
        self.cartera = {}  # Diccionario donde las claves son los símbolos de las acciones y los valores son instancias de Accion
        self.transacciones = []  # Lista para almacenar transacciones realizadas

    def comprar(self, accion: Accion, cantidad: int):
        """
        Permite al inversor comprar acciones. Verifica si tiene suficiente capital.
        
        Parámetros:
        - accion: La acción que desea comprar
        - cantidad: La cantidad de acciones que desea comprar
        """
        if cantidad <= 0:
            raise ValueError("La cantidad de acciones a comprar debe ser mayor que 0")
        
        costo_total = accion.precio_actual * cantidad
        
        if self.capital >= costo_total:
            self.capital -= costo_total  # Restamos el dinero del capital
            if accion.simbolo in self.cartera:
                self.cartera[accion.simbolo][1] += cantidad
            else:
                self.cartera[accion.simbolo] = [accion, cantidad]
            
            # Registrar la transacción en la base de datos
            self.registrar_transaccion("Compra", accion, cantidad)
            print(f"{self.nombre} ha comprado {cantidad} acciones de {accion.nombre}.")
        else:
            raise ValueError(f"No tienes suficiente dinero para comprar {cantidad} acciones de {accion.nombre}.")

    def vender(self, accion: Accion, cantidad: int):
        """
        Permite al inversor vender acciones. Verifica si tiene suficientes acciones.
        
        Parámetros:
        - accion: La acción que desea vender
        - cantidad: La cantidad de acciones que desea vender
        """
        if cantidad <= 0:
            raise ValueError("La cantidad de acciones a vender debe ser mayor que 0")

        if accion.simbolo in self.cartera and self.cartera[accion.simbolo][1] >= cantidad:
            self.capital += accion.precio_actual * cantidad
            self.cartera[accion.simbolo][1] -= cantidad  # Restamos las acciones de la cartera
            
            # Si la cantidad es 0, eliminamos la acción de la cartera
            if self.cartera[accion.simbolo][1] == 0:
                del self.cartera[accion.simbolo]  # Eliminamos la acción si ya no quedan acciones
            
            # Registrar la transacción en la base de datos
            self.registrar_transaccion("Venta", accion, cantidad)
            print(f"{self.nombre} ha vendido {cantidad} acciones de {accion.nombre}.")
        else:
            print(f"{self.nombre} no tiene suficientes acciones de {accion.nombre} para vender.")

    def mostrar_cartera(self):
        """
        Devuelve un resumen del contenido de la cartera del inversor.
        """
        contenido = f"Cartera de {self.nombre}:\n"
        for accion, (instancia_accion, cantidad) in self.cartera.items():
            contenido += f"- {instancia_accion.nombre} ({accion}): {cantidad} acciones\n"
        contenido += f"Capital disponible: {self.capital:.2f}€"
        return contenido

    def registrar_transaccion(self, tipo: str, accion: Accion, cantidad: int):
        from .transaccion import Transaccion 
        from database.db_manager import guardar_transaccion
        #los ponemos aquí para que no haya circular import
        """
        Registra la transacción en el historial del inversor y en la base de datos.
        
        Parámetros:
        - tipo: Tipo de transacción ("Compra" o "Venta")
        - accion: Acción relacionada con la transacción
        - cantidad: Cantidad de acciones involucradas
        """
        # Crear la transacción
        transaccion = Transaccion(self, accion, cantidad, accion.precio_actual)
        
        # Guardar la transacción en la base de datos
        guardar_transaccion(transaccion)
        
        # Registra la transacción en memoria
        self.transacciones.append(transaccion)

    def __str__(self):
        return f"Inversor {self.nombre} - Capital: {self.capital:.2f}€ - Cartera: {self.cartera}"

    def __add__(self, other):
        """
        Sobrecarga para el operador +. Permite comprar acciones usando la sintaxis: inversor + (accion, cantidad)
        
        Parámetros:
        - other: Tupla que contiene la acción y la cantidad a comprar
        """
        if isinstance(other, tuple) and len(other) == 2:
            accion, cantidad = other
            self.comprar(accion, cantidad)
        else:
            raise TypeError("Se debe usar la sintaxis: inversor + (accion, cantidad)")

    def __sub__(self, other):
        """
        Sobrecarga para el operador -. Permite vender acciones usando la sintaxis: inversor - (accion, cantidad)
        
        Parámetros:
        - other: Tupla que contiene la acción y la cantidad a vender
        """
        if isinstance(other, tuple) and len(other) == 2:
            accion, cantidad = other
            self.vender(accion, cantidad)
        else:
            raise TypeError("Se debe usar la sintaxis: inversor - (accion, cantidad)")
