from .accion import Accion
from .inversor import Inversor
from datetime import datetime

class Transaccion:
    """
    Clase Transaccion que representa una operación bursátil realizada por un inversor.

    Atributos
    -----------------
    inversor : Inversor
        El inversor que realiza la operación.
    accion : Accion
        La acción que se compra o vende.
    cantidad : int
        Número de acciones que se compran o venden.
    precio : float
        Precio por acción en el momento de la transacción.
    fecha_hora : datetime
        Fecha y hora en la que se realiza la operación.

    Métodos
    -----------------
    calcular_total()
        Calcula el total de la operación (precio * cantidad).
    validar_transaccion()
        Verifica si el inversor tiene suficiente capital.
    ejecutar_transaccion()
        Ejecuta la operación si es válida, actualizando la cartera y el capital.
    __str__()
        Devuelve una descripción legible de la transacción.
    """

    def __init__(self, inversor: Inversor, accion: Accion, cantidad: int, precio: float):
        """
        Constructor de la clase Transaccion.

        Parámetros
        ----------------
        inversor : Inversor
            Objeto de la clase Inversor que realiza la transacción.
        accion : Accion
            Objeto de la clase Accion que se compra o vende.
        cantidad : int
            Número de acciones involucradas en la transacción.
        precio : float
            Precio por acción en el momento de la transacción.
        """
        self.inversor = inversor
        self.accion = accion
        self.cantidad = cantidad
        self.precio = precio
        self.fecha_hora = datetime.now()  # Fecha y hora de la transacción

    def calcular_total(self) -> float:
        """
        Calcula el costo total de la transacción.

        Returns
        ---------
        float
            Total en euros (precio * cantidad)
        """
        return self.cantidad * self.precio

    def validar_transaccion(self):
        """
        Verifica si el inversor tiene suficiente capital para realizar la compra.

        Returns
        -----------------
        bool
            True si el capital es suficiente, False si no.
        """
        return self.inversor.capital >= self.calcular_total()

    def ejecutar_transaccion(self):
        """
        Ejecuta la transacción en caso de ser válida, actualizando el capital del inversor
        y su cartera de acciones.

        Si no es válida, informa que no hay fondos suficientes.
        """
        if self.validar_transaccion():
            self.inversor.capital -= self.calcular_total()  # Descontamos el dinero del inversor
            # Actualizamos la cartera del inversor
            if self.accion.simbolo in self.inversor.cartera:
                self.inversor.cartera[self.accion.simbolo][1] += self.cantidad  # Sumamos las acciones
            else:
                self.inversor.cartera[self.accion.simbolo] = [self.accion, self.cantidad]  # Añadimos nueva acción a la cartera
            print(f"Transacción realizada correctamente: {self}")
        else:
            print("Fondos insuficientes para realizar la operación")

    def __str__(self):
        """
        Devuelve una representación en cadena de la transacción.

        Returns
        -----------------
        str
            Descripción legible con fecha, nombre, acción, cantidad y precio.
        """
        return (f"{self.inversor.nombre} compró {self.cantidad} acciones de {self.accion.nombre} "
                f"a {self.precio}$ cada una, el {self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}.")
