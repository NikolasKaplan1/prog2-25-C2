from .accion import Accion
from .transaccion import Transaccion
from typing import List



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
        Diccionario con las acciones que posee (clave: símbolo, valor: [Accion, cantidad]).
    
    transacciones : list[Transaccion]
    
    
    Métodos
    -------------
    comprar(accion, cantidad)
        Compra acciones si tiene suficiente capital.

    vender(accion, cantidad)
        Vende acciones si tiene suficientes.

    mostrar_cartera()
        Muestra el contenido de la cartera del inversor.
    
    registrar_transaccion()
        Registra una transacción en el historial

    __str__()
        Muestra el resumen del inversor.
    
    __add__()
        Sobrecarga para comprar acciones con +.
    
    __sub__() 
        Sobrecarga para vender acciones con -.

    """
    def __init__(self, nombre:str, capital:float):
        """
        Parámetros
        ---------------
        nombre
            Nombre del inversor.

        capital
            Cantidad de dinero que tiene el inversor en su cuenta.

        """
        self.nombre = nombre
        self.capital = capital
        self.cartera = {} # clave: simbolo, valor: [accion, cantidad]
        self.transacciones = [] # lista de transacciones realizadas


    def comprar(self, accion: Accion, cantidad: int):
        
        """ Compra acciones si tiene suficiente capital"""
        
        costo_total = accion.precio_actual * cantidad
        if self.capital >= costo_total:
            self.capital -= costo_total  #se puede adquirir

            if accion.simbolo in self.cartera:
                self.cartera[accion.simbolo][1] += cantidad
            else:
                self.cartera[accion.simbolo] = [accion, cantidad]
            
            self.registrar_transaccion("Compra", accion, cantidad)
            
        else:
            raise ValueError ("No tienes suficiente dinero en cuenta para comprar")


    def vender(self, accion:Accion, cantidad:int):
        
        """ Vende acciones si el inversor tiene suficientes"""
        
        if accion.simbolo in self.cartera and self.cartera[accion.simbolo][1] >= cantidad:
            self.capital += accion.precio_actual * cantidad
            self.cartera[accion.simbolo][1] -= cantidad # se descuenta de la cartera al venderla
            self.registrar_transaccion("Venta", accion, cantidad)
        else:
            print("No tienes suficientes acciones para vender")
    
    def mostrar_cartera(self):
        """ Devuelve un resumen del contenido de la cartera """
        contenido = "Cartera de " + self.nombre + ":\n"
        for i in self.cartera:
            accion = self.cartera[i][0]
            cantidad = self.cartera[i][1]
            contenido += "- " + accion.nombre + " (" + i + "): " + str(cantidad) + " acciones\n"
        contenido += "Capital disponible: " + str(round(self.capital, 2)) + "€"
        return contenido
    
    def registrar_transaccion(self, tipo: str, accion: Accion, cantidad: int):
     
        """ Registra la transaccion en la lista de historial"""
        if tipo == "Venta":
            cantidad = -cantidad
        transaccion = Transaccion(self, accion, cantidad, accion.precio_actual)
        self.transacciones.append(transaccion)
    
    def __str__(self):
        return f"Inversor {self.nombre} - Capital: {round(self.capital, 2)}€ - Cartera: {self.cartera}"
    
    def __add__(self, other): # inversor adquiere x accion de x cantidad
        """
        Permite comprar acciones usando el operador +.

        Parámetros
        -------------
            other : tuple
                Tupla con la acción y la cantidad (accion, cantidad)
        """

        if isinstance(other, tuple) and len(other) == 2: # verificamos si el valor other es una tupla y tiene 2 elementos
            accion, cantidad = other
            self.comprar(accion, cantidad)

        else:
            raise TypeError ("Debes usar: inversor + (accion, cantidad)")

    def __sub__(self, other):
        if isinstance(other, tuple) and len(other) == 2:
            accion, cantidad = other
            self.vender(accion, cantidad)
        else:
            raise TypeError ("Debes usar: inversor - (accion, cantidad)")



class InversorAgresivo(Inversor): # Busca ganancias rápidas y grandes
    """
    Inversor con estrategia agresiva:
    Prefiere comprar acciones de precio alto (potencial de ganancia rápido)
    """

    def recomendar_compra(self):
        """
        Recomienda las acciones más caras de la cartera

        Returns
        ---------
        list[str]
            lista con los nombres y precios de las acciones recomendadas

        """
        acciones = list(self.cartera.values())
        lista_precios = []
        for accion, _ in acciones:
            lista_precios.append([accion, accion.precio_actual])

        for i in range(len(lista_precios)):
            for j in range(i + 1, len(lista_precios)):
                if lista_precios[i][1] < lista_precios[j][1]: # ordena de mayor a menor (estrategia agresiva)
                    lista_precios[i], lista_precios[j] = lista_precios[j], lista_precios[i]

        recomendaciones = []
        for i in range(min(2, len(lista_precios))):
            accion = lista_precios[i][0]
            recomendaciones.append(accion.nombre + " a " + str(round(accion.precio_actual, 2)) + "€")

        return recomendaciones

class InversorPasivo(Inversor): # prefiere seguridad y estabilidad
    def recomendar_compra(self):
        """
        Recomienda las dos acciones más baratas de la cartera.

        Returns
        -------------
        list[str]
            Lista con nombre y precio de las acciones recomendadas.
        """
        acciones = list(self.cartera.values())  # lista de [Accion, cantidad]

        lista_precios = []
        for accion, _ in acciones:
            lista_precios.append([accion, accion.precio_actual])

        for i in range(len(lista_precios)):
            for j in range(i + 1, len(lista_precios)):
                if lista_precios[i][1] > lista_precios[j][1]:
                    lista_precios[i], lista_precios[j] = lista_precios[j], lista_precios[i]

        recomendaciones = []
        for i in range(min(2, len(lista_precios))):
            accion = lista_precios[i][0]
            recomendaciones.append(accion.nombre + " a " + str(round(accion.precio_actual, 2)) + "€")

        return recomendaciones
