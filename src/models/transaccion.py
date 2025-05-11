from .accion import Accion
from .inversor import Inversor
from datetime import datetime
from typing import Union

class Transaccion:
    """
    Representa una transacción de compra de acciones realizada por un inversor.
    Registra la cantidad, el precio de la acción en el momento de la operación, y almacena la fecha y hora exacta de ejecución.

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
    _fecha_hora : datetime
        Fecha y hora en la que se realiza la operación.

    Methods
    -------
    calcular_total()
        Calcula el total de la operación (precio * cantidad).
    validar_transaccion()
        Verifica si el inversor tiene suficiente capital.
    ejecutar_transaccion()
        Ejecuta la operación si es válida, actualizando la cartera y el capital.
    __str__()
        Devuelve una descripción legible de la transacción.
    """

    def __init__(self, inversor: Inversor, accion: Accion, cantidad: int) -> None:
        """
        Inicializa una transacción con el inversor, la acción y la cantidad de acciones involucradas.

        Parameters
        ----------
        inversor : Inversor
            Objeto de la clase Inversor que realiza la transacción.
        accion : Accion
            Objeto de la clase Accion que se compra o vende.
        cantidad : int
            Número de acciones involucradas en la transacción.
        """
        self.inversor = inversor
        self.accion = accion
        self.cantidad = cantidad
        self.precio = accion._precio_actual
        self._fecha_hora = datetime.now()  # Fecha y hora de la transacción

    def calcular_total(self) -> float:
        """
        Calcula el coste total de la operación (precio por cantidad).

        Returns
        -------
        float
            Total de la transacción en euros (precio * cantidad)
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
        return self.inversor._Inversor__capital >= self.calcular_total()

    def ejecutar_transaccion(self) -> None:
        """
        Ejecuta la transacción en caso de ser válida, actualizando el capital del inversor
        y su cartera de acciones.

        Si no es válida, informa que no hay fondos suficientes.

        Returns 
        -------
        None

        Raises
        ------
        ValueError
            Si el capital disponible del inversor es insuficiente para cubrir el costo de la operación.
        """
        if not self.validar_transaccion():
            raise ValueError(
                f"{self.inversor._nombre} no tiene fondos suficientes para comprar "
                f"{self.cantidad} acciones de {self.accion.nombre}."
            )

        self.inversor._Inversor__capital -= self.calcular_total()  # Descontamos el dinero del inversor
        # Actualizamos la cartera del inversor
        if self.accion.simbolo in self.inversor._Inversor__cartera:
            self.inversor._Inversor__cartera[self.accion.simbolo][1] += self.cantidad  # Sumamos las acciones
        else:
            self.inversor._Inversor__cartera[self.accion.simbolo] = [self.accion, self.cantidad]  # Añadimos nueva acción a la cartera
        print(f"Transacción realizada correctamente: {self}")
    
    def __str__(self) -> str:
        """
        Devuelve una representación en cadena de la transacción.
        Incluyendo el nombre del inversor, nombre de la accion, cantidad, precio por unidad y fecha.

        Returns
        -------
        str
            Cadena descriptiva de la transacción realizada.
        """
        return (f"{self.inversor._nombre} compró {self.cantidad} acciones de {self.accion.nombre} "
                f"a {self.precio}$ cada una, el {self._fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}.")

    def __getitem__(self, key: str) -> Union[str, int, float, datetime]:
        """
        Permite acceder a los atributos de la transacción como si fuera un diccionario.
        
        Parameters
        ----------
        key : str 
            Clave del dato que se desea obtener
        
        Returns
        -------
        Cualquier tipo
            El valor asociado a la clave especificada
        
        Raises
        ------
        KeyError
            Si la clave no es válida
        """

        if key == 'inversor':
            return self.inversor._nombre
        elif key == 'accion':
            return self.accion.nombre
        elif key == 'simbolo':
            return self.accion.simbolo
        elif key == 'cantidad':
            return self.cantidad 
        elif key == 'precio':
            return self.precio
        elif key == 'fecha':
            return self._fecha_hora
        else:
            raise KeyError(
                f"{key} no es un campo válido en Transaccion."
            )

