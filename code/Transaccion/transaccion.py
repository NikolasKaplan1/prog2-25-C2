from datetime import datetime


class Transaccion:
    def __init__(self, inversor, accion, cantidad, precio):
    def __init__(self, inversor: Inversor, accion: Accion, cantidad: int, precio: float):
        """
        Constructor de la clase Transaccion.

        :param inversor: Objeto de la clase inversor que realiza la transaccion.
        :para accion: Objeto de la clase accion que se compra o vende
        :param cantidad: Numero de acciones involucradas en la transaccion
        :param precio: Precio de la accion en el momento de la transaccion


        """
        self.inversor = inversor
        self.accion = accion
        self.cantidad = cantidad
        self.precio = precio
        self.fecha_hora = datetime.now() # fecha y hora de la transacción


    def calcular_total(self):
        """
        Calcula el costo total de la transaccion.
        """
        return self.cantidad * self.precio

    def validar_transaccion(self):
        """
        Verifica si el inversor tiene suficiente capital para realizar la compra.
        """
        return self.inversor.capital >= self.calcular_total()

    def ejecutar_transaccion(self):
        """
        Ejecuta la transacción en caso de ser válida, actualizando el capital del inversor
        """
        if self.validar_transaccion():
            self.inversor.capital -= self.calcular_total()
            self.inversor.cartera.append(self.accion)
            print("Transaccion realizada correctamente: {self}")

        else:
            print("Fondos insuficientes para realizar la operación")

    def __str__(self):
        """
        Devuelve una representación en cadena de la transacción.
        """
        return (f"{self.inversor.nombre} compró {self.cantidad} acciones de {self.accion.nombre} "
                "a {self.precio}$ cada una, el {self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}.")
    