
from acciones import Accion


class Inversor:
    def __init__(self, nombre:str, capital:float):
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