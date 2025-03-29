from datetime import date

class Accion:
    def __init__(self, simbolo: str, nombre: str, precio_actual: float, historial_precios: dict[str, float]): #el str sería la fecha y el float el valor de la acción en esa fecha
        self.simbolo = simbolo
        self.nombre = nombre
        self.precio_actual = precio_actual
        self.historial_precios = historial_precios
    def actualizar_precio(self,nuevo_precio: float):
        self.historial_precios[date.today()] = nuevo_precio
        self.precio_actual = nuevo_precio
    def str(self):
        print(f"El logo de la acción de la empresa {self.nombre} es {self.precio_actual} y el precio actual de dicha acción es {self.precio_actual}. El historial de precios es ", end = '')
        for key, value in self.historial_precios.items():
            print(f"{key}: {value}", end = '')

