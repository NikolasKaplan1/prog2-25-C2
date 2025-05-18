from .accion import Accion
from .inversor import Inversor
from datetime import datetime
from typing import Union

from datetime import datetime
from typing import Union
from .accion import Accion
from .inversor import Inversor

class Transaccion:
    """
<<<<<<< Updated upstream
    Representa una transacción de compra de acciones realizada por un inversor.
    Registra la cantidad, el precio de la acción en el momento de la operación, y almacena la fecha y hora exacta de ejecución.
=======
<<<<<<< Updated upstream
    Clase Transaccion que representa una operación bursátil realizada por un inversor.
=======
    Representa una transacción de compra o venta de acciones realizada por un inversor.
>>>>>>> Stashed changes
>>>>>>> Stashed changes

    Attributes
    ----------
    inversor : Inversor
        El inversor que realiza la operación.
    accion : Accion
        La acción que se compra o vende.
    cantidad : int
        Número de acciones involucradas.
    precio : float
        Precio por acción en el momento de la transacción.
<<<<<<< Updated upstream
    _fecha_hora : datetime
=======
<<<<<<< Updated upstream
    fecha_hora : datetime
=======
    tipo : str
        Tipo de operación: "Compra" o "Venta".
    _fecha_hora : datetime
>>>>>>> Stashed changes
>>>>>>> Stashed changes
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
        Permite acceder a los atributos como si fuera un diccionario.
    __str__()
        Devuelve una descripción legible de la transacción.
    """

<<<<<<< Updated upstream
    def __init__(self, inversor: Inversor, accion: Accion, cantidad: int) -> None:
        """
        Inicializa una transacción con el inversor, la acción y la cantidad de acciones involucradas.
=======
<<<<<<< Updated upstream
    def __init__(self, inversor: Inversor, accion: Accion, cantidad: int):
        """
        Constructor de la clase Transaccion.
=======
    def __init__(self, inversor: Inversor, accion: Accion, cantidad: int, precio: float, tipo: str) -> None:
        """
        Inicializa una transacción con el inversor, acción, cantidad y tipo.
>>>>>>> Stashed changes
>>>>>>> Stashed changes

        Parameters
        ----------
        inversor : Inversor
            Objeto inversor que realiza la operación.
        accion : Accion
            Objeto acción sobre la que se realiza la operación.
        cantidad : int
<<<<<<< Updated upstream
            Número de acciones involucradas en la transacción.
<<<<<<< Updated upstream
=======
        precio : float
            Precio por acción en el momento de la transacción.
=======
            Cantidad de acciones involucradas.
        precio : float, optional
            Precio por acción. Por defecto, el precio actual de la acción.
        tipo : str, optional
            Tipo de transacción: "Compra" o "Venta". Por defecto "Compra".
>>>>>>> Stashed changes
>>>>>>> Stashed changes
        """
        self.inversor = inversor
        self.accion = accion
        self.cantidad = cantidad
<<<<<<< Updated upstream
        self.precio = accion._precio_actual
        self._fecha_hora = datetime.now()  # Fecha y hora de la transacción

    def calcular_total(self) -> float:
        """
        Calcula el coste total de la operación (precio por cantidad).
=======
<<<<<<< Updated upstream
        self.precio = accion.precio_actual
        self.fecha_hora = datetime.now()  # Fecha y hora de la transacción

    def calcular_total(self) -> float:
        """
        Calcula el costo total de la transacción.
=======
        self.precio = precio if precio is not None else accion._precio_actual
        self.tipo = tipo
        self._fecha_hora = datetime.now()

    def calcular_total(self) -> float:
        """
        Calcula el total de la transacción.
>>>>>>> Stashed changes
>>>>>>> Stashed changes

        Returns
        -------
        float
<<<<<<< Updated upstream
            Total de la transacción en euros (precio * cantidad)
=======
<<<<<<< Updated upstream
            Total en euros (precio * cantidad)
=======
            Total a pagar o recibir (precio * cantidad).
>>>>>>> Stashed changes
>>>>>>> Stashed changes
        """
        return self.cantidad * self.precio

    def validar_transaccion(self) -> bool:
        """
        Verifica si el inversor tiene suficiente capital para realizar la compra.

        Returns
        -------
        bool
            True si el capital es suficiente, False en caso contrario.
        """
        return self.inversor._Inversor__capital >= self.calcular_total()

    def ejecutar_transaccion(self) -> None:
        """
<<<<<<< Updated upstream
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
<<<<<<< Updated upstream
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

=======
        return (f"{self.inversor.nombre} compró {self.cantidad} acciones de {self.accion.nombre} "
                f"a {self.precio}$ cada una, el {self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}.")
=======
        Ejecuta la transacción: actualiza el capital y la cartera del inversor.

        Raises
        ------
        ValueError
            Si no hay fondos suficientes para la compra.
        """
        if not self.validar_transaccion():
            raise ValueError(
                f"{self.inversor._nombre} no tiene fondos suficientes para comprar "
                f"{self.cantidad} acciones de {self.accion.nombre}."
            )

        # Descontar dinero del inversor
        self.inversor._Inversor__capital -= self.calcular_total()

        # Actualizar cartera
        if self.accion.simbolo in self.inversor._Inversor__cartera:
            accion_existente, cantidad_existente = self.inversor._Inversor__cartera[self.accion.simbolo]
            self.inversor._Inversor__cartera[self.accion.simbolo] = (accion_existente, cantidad_existente + self.cantidad)
        else:
            self.inversor._Inversor__cartera[self.accion.simbolo] = (self.accion, self.cantidad)

    def __getitem__(self, key: str) -> Union[str, int, float, datetime]:
        """
        Permite acceder a los atributos como si la transacción fuera un diccionario.

        Parameters
        ----------
        key : str
            Clave del atributo: 'inversor', 'accion', 'simbolo', 'cantidad', 'precio', 'fecha'

        Returns
        -------
        Union[str, int, float, datetime]
            Valor del campo correspondiente.

        Raises
        ------
        KeyError
            Si se accede a un campo inexistente.
        """
>>>>>>> Stashed changes
        if key == 'inversor':
            return self.inversor._nombre
        elif key == 'accion':
            return self.accion.nombre
        elif key == 'simbolo':
            return self.accion.simbolo
        elif key == 'cantidad':
<<<<<<< Updated upstream
            return self.cantidad 
=======
            return self.cantidad
>>>>>>> Stashed changes
        elif key == 'precio':
            return self.precio
        elif key == 'fecha':
            return self._fecha_hora
        else:
<<<<<<< Updated upstream
            raise KeyError(
                f"{key} no es un campo válido en Transaccion."
            )

=======
            raise KeyError(f"{key} no es un campo válido en Transaccion.")

    def __str__(self) -> str:
        """
        Devuelve una representación legible de la transacción.

        Returns
        -------
        str
            Texto con la operación realizada.
        """
        tipo = "Compró" if self.tipo.lower() == "compra" else "Vendió"
        return (f"{self.inversor._nombre} {tipo} {self.cantidad} acciones de {self.accion.nombre} "
                f"a {self.precio}€ cada una, el {self._fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}.")


>>>>>>> Stashed changes
>>>>>>> Stashed changes
