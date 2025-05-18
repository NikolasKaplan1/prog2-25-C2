from .accion import Accion
from typing import List

from .accion import Accion
from typing import List


class Inversor:
    """
    La clase Inversor representa a una persona que invierte en el mercado financiero.
    Permite gestionar su capital y su cartera de inversión.

    Attributes
    ----------
    _nombre : str
        Nombre del inversor (acceso protegido).
    __capital : float
        Capital disponible del inversor (acceso privado).
    __cartera : dict[str, tuple[Accion, int]]
        Diccionario donde las claves son los símbolos de las acciones y los valores son instancias de Accion (acceso privado).
    _transacciones : list
        Historial de transacciones realizadas (acceso protegido).

    Methods
    -------
    comprar(accion: Accion, cantidad: int)
        muestra la compra y cantidad de acciones.
    vender(accion: Accion, cantidad: int)
        vendes una cantidad de acciones.
    mostrar_cartera()
        te enseña la cartera del inversor.
    registrar_transaccion(tipo, accion, cantidad)
        registrar una transaccion efectuada.
    __add__(other: tuple[Accion,int])
        método para comprar una cantidad de acciones.
    __sub__(other: tuple[Accion, int])
        método para vender una cantidad de acciones.
    __contains__(accion: Accion)
        Método para saber si un inversor contiene una acción.
    __eq__(accion: Accion, cantidad: int)
        Método para saber si dos inversores han invertido en las mismas empresas.
    """

    def __init__(self, nombre: str, capital: float) -> None:
        """
        Inicializa un inversor con nombre y capital inicial.

        Parameters
        ----------
        nombre : str
            Nombre del inversor.

        capital : float
            Capital inicial del inversor.
        """

        self._nombre = nombre
        self.__capital = capital
        # Diccionario donde las claves son los símbolos de las acciones y los valores son instancias de Accion
        self.__cartera: dict[str, tuple[Accion, int]] = {}
        # Lista para almacenar transacciones realizadas
        self._transacciones = []

    @property
    def capital(self):
        return self.__capital

    def comprar(self, accion: Accion, cantidad: int) -> None:
        """
        Permite al inversor comprar acciones. Verifica si tiene suficiente capital.

        Parameters
        ----------
        accion : Accion
            Objeto acción que desea commprar.
        cantidad : int
            La cantidad de acciones que desea comprar.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Si la cantidad es menor o igual a cero o si no hay capital suficiente.

        """
        if cantidad <= 0:
            raise ValueError("La cantidad de acciones a comprar debe ser mayor que 0")

        costo_total = accion._precio_actual * cantidad

        if self.__capital >= costo_total:
            self.__capital -= costo_total  # Restamos el dinero del capital
            if accion.simbolo in self.__cartera:
                accion_existente, cantidad_existente = self.__cartera[accion.simbolo]
                self.__cartera[accion.simbolo] = (accion_existente, cantidad_existente + cantidad)
            else:
                self.__cartera[accion.simbolo] = (accion, cantidad)

            # Registrar la transacción en la base de datos
            self.registrar_transaccion("Compra", accion, cantidad)
        else:
            raise ValueError(f"No tienes suficiente dinero para comprar {cantidad} acciones de {accion.nombre}.")

    def vender(self, accion: Accion, cantidad: int, tipo: str = "Venta") -> None:
        """
        Permite al inversor vender acciones. Verifica si tiene suficientes acciones.

        Parameters
        ----------
        accion : Accion
            La acción que desea vender.
        cantidad : int
            La cantidad de acciones que desea vender.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Si no tienes acciones suficientes a vender o la cantidad no es válida.
        """

        if cantidad <= 0:
            raise ValueError("La cantidad de acciones a vender debe ser mayor que 0")

        if accion.simbolo in self.__cartera:
            accion_existente, cantidad_existente = self.__cartera[accion.simbolo]
            if cantidad_existente >= cantidad:
                nueva_cantidad = cantidad_existente - cantidad
                self.__capital += accion._precio_actual * cantidad
                if nueva_cantidad > 0:
                    self.__cartera[accion.simbolo] = (accion_existente, nueva_cantidad)
                else:
                    del self.__cartera[accion.simbolo]
                self.registrar_transaccion(tipo, accion, cantidad)
            else:
                raise ValueError(f"No tienes suficientes acciones de {accion.nombre} para vender.")
        else:
            raise ValueError(f"No tienes acciones de {accion.nombre} para vender.")

    def mostrar_cartera(self) -> str:
        """
        Devuelve un resumen del contenido de la cartera del inversor.

        Returns
        -------
        str
            Texto con el contenido de la cartera y capital restante.
        """
        contenido = f"Cartera de {self._nombre}:\n"
        for accion, (instancia_accion, cantidad) in self.__cartera.items():
            contenido += f"- {instancia_accion.nombre} ({accion}): {cantidad} acciones\n"
        contenido += f"Capital disponible: {self.__capital:.2f}€"
        return contenido

    def registrar_transaccion(self, tipo: str, accion: Accion, cantidad: int) -> None:
        """
        Registra la transacción en el historial del inversor y en la base de datos.

        Parameters
        ----------

        tipo : str
            Tipo de transacción ("Compra" o "Venta")
        accion : Accion
            Acción relacionada con la transacción
        cantidad : int
            Cantidad de acciones involucradas

        Returns
        -------
        None

        """
        # los ponemos aquí para que no haya circular import
        from .transaccion import Transaccion

        transaccion = Transaccion(self, accion, cantidad, accion._precio_actual, tipo)
        # Registra la transacción en memoria
        self._transacciones.append(transaccion)

    def __str__(self) -> str:
        """
        Devuelve una representación textual del inversor.

        Returns
        -------
        str
            Cadena con información del inversor y cartera.
        """
        return f"Inversor {self._nombre} - Capital: {self.__capital:.2f}€ - Cartera: {self.__cartera}"

    def __add__(self, other: tuple[Accion, int]) -> 'Inversor':
        """
        Sobrecarga para el operador +. Permite comprar acciones usando la sintaxis: inversor + (accion, cantidad)

        Parameters
        ----------
            other : Tuple[Accion, int]
                Tupla que contiene el objeto Accion y la cantidad a comprar.

        Raises
        ------
        TypeError
            Si el argumento no es una tupla válida con (Accion, int).
        """
        if isinstance(other, tuple) and len(other) == 2:
            accion, cantidad = other
            self.comprar(accion, cantidad)
        else:
            raise TypeError("Se debe usar la sintaxis: inversor + (accion, cantidad)")

    def __sub__(self, other: tuple[Accion, int]) -> 'Inversor':
        """
        Sobrecarga para el operador -. Permite vender acciones usando la sintaxis: inversor - (accion, cantidad)

        Parameters
        ----------
            other : Tuple[Accion, int]
                Tupla que contiene el objeto Accion y la cantidad a vender.

        Raises
        ------
        TypeError
            Si el argumento no es una tupla válida con (Accion, int).
        """
        if isinstance(other, tuple) and len(other) == 2:
            accion, cantidad = other
            self.vender(accion, cantidad)
        else:
            raise TypeError("Se debe usar la sintaxis: inversor - (accion, cantidad)")

    def __contains__(self, simbolo: str) -> bool:
        """
        Permite verificar si el inversor posee acciones de una empresa a través de su símbolo.

        Parameters
        ----------
        simbolo : str
            Símbolo de la acción a buscar en la cartera.

        Returns
        -------
        bool
            True si el símbolo está en la cartera, False en caso contrario.
        """
        return simbolo in self._Inversor__cartera

    def __eq__(self, other: object) -> bool:
        """
        Compara si dos inversores han invertido en las mismas empresas,
        independientemente de la cantidad de acciones que posean.
        La comparación se realiza mediante los símbolos de las acciones en la cartera.

        Parameters
        ----------
        other : object
            Otro objeto a comparar

        Returns
        -------
        bool
            True si ambos inversor tienen acciones en las mismas empresas.

        """

        if not isinstance(other, Inversor):
            return False
        simbolos_self = sorted(self._Inversor__cartera.keys())
        simbolos_other = sorted(other._Inversor__cartera.keys())
        return simbolos_self == simbolos_other