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
