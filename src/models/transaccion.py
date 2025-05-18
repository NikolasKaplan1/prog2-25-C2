from .accion import Accion
from .inversor import Inversor
from datetime import datetime


class Transaccion:
    """
    Clase Transaccion que representa una operación bursátil realizada por un inversor.

    Attributes
    ----------
    inversor : Inversor
        El inversor que realiza la operación.
    accion : Accion
        La acción que se compra o vende.
    cantidad : int
        Número de acciones que se compran o venden.
    precio : float
        Precio por acción en el momento de la transacción.
    tipo : str
        Tipo de transacción: "Compra" o "Venta".
    fecha_hora : datetime
        Fecha y hora en la que se realiza la operación.

    Methods
    -------
    calcular_total()
        Calcula el total de la operación (precio * cantidad).
    validar_transaccion()
        Verifica si el inversor tiene suficiente capital.
    ejecutar_transaccion()
        Ejecuta la operación si es válida, actualizando la cartera y el capital.
    __getitem__(key)
        Permite acceder a atributos por clave.
    __str__()
        Devuelve una descripción legible de la transacción.
    """

    def __init__(self, inversor: Inversor, accion: Accion, cantidad: int, precio: float, tipo: str):
        """
        Constructor de la clase Transaccion.

        Parameters
        ----------
        inversor : Inversor
            Objeto que realiza la transacción.
        accion : Accion
            Acción sobre la que se realiza la operación.
        cantidad : int
            Cantidad de acciones involucradas.
        precio : float
            Precio por acción al momento de la operación.
        tipo : str
            "Compra" o "Venta"
        """
        self.inversor = inversor
        self.accion = accion
        self.cantidad = cantidad
        self.precio = precio
        self.tipo = tipo
        self.fecha_hora = datetime.now()

    def calcular_total(self) -> float:
        """
        Calcula el costo total de la transacción.

        Returns
        ---------
        float
            Total en euros (precio * cantidad)
        """
        return self.cantidad * self.precio

    def validar_transaccion(self) -> bool:
        """
        Verifica si el inversor tiene suficiente capital para realizar la compra.

        Returns
        -------
        bool
            True si el capital es suficiente, False si no.
        """
        return self.inversor.capital >= self.calcular_total()

    def __getitem__(self, key: str) -> Union[str, int, float, datetime]:
        """
        Permite acceder a los atributos de la transacción como si fuera un diccionario.

        Parameters
        ----------
        key : str
            Nombre del campo a consultar: 'inversor', 'accion', 'simbolo', 'cantidad', 'precio', 'fecha'.

        Returns
        -------
        Union[str, int, float, datetime]
            Valor del campo solicitado.

        Raises
        ------
        KeyError
            Si el campo no existe.
        """
        if key == "inversor":
            return self.inversor._nombre
        elif key == "accion":
            return self.accion.nombre
        elif key == "simbolo":
            return self.accion.simbolo
        elif key == "cantidad":
            return self.cantidad
        elif key == "precio":
            return self.precio
        elif key == "fecha":
            return self.fecha_hora
        else:
            raise KeyError(f"{key} no es un campo válido en Transaccion.")

    def __str__(self) -> str:
        """
        Devuelve una descripción legible de la transacción.

        Returns
        ---------
        str
            Texto con la operación realizada.
        """
        verbo = "compró" if self.tipo.lower() == "compra" else "vendió"
        return (f"{self.inversor._nombre} {verbo} {self.cantidad} acciones de {self.accion.nombre} "
                f"a {self.precio:.2f}€ cada una, el {self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}.")