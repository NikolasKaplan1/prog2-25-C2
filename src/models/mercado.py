import random
from .accion import Accion
from typing import Union, Optional
from abc import ABC, abstractmethod


class BaseMercado(ABC):
    """
    Interfaz abstracta que define el comportamiento de un mercado financiero.

    Cualquier clase que herede de BaseMercado deberá implementar los métodos
    necesarios para registrar acciones, obtener precios, simular movimientos
    y manejar bancarrotas.

    Methods
    -------
    registrar_accion(accion: Accion) -> None
        Registra una nueva acción en el mercado.

    obtener_precio(simbolo: str) -> Union[float, str]
        Obtiene el precio de una acción por su símbolo.

    bancarrota(simbolo: str) -> Union[None, str]
        Elimina una acción del mercado y la declara en bancarrota.

    simular_movimientos() -> None
        Simula fluctuaciones aleatorias en los precios de las acciones.
    """

    @abstractmethod
    def registrar_accion(self, accion: Accion) -> None:
        """
        Registra una acción en el mercado.

        Parameters
        ----------
        accion : Accion
            La acción que se desea registrar.
        """
        pass

    @abstractmethod
    def obtener_precio(self, simbolo: str) -> Union[float, str]:
        """
        Devuelve el precio actual de una acción por su símbolo.

        Parameters
        ----------
        simbolo : str
            Símbolo de la acción a consultar.

        Returns
        -------
        float or str
            Precio de la acción o un mensaje si no se encuentra.
        """
        pass

    @abstractmethod
    def bancarrota(self, simbolo: str) -> Union[None, str]:
        """
        Declara en bancarrota una acción y la elimina del mercado.

        Parameters
        ----------
        simbolo : str
            Símbolo de la acción a declarar en bancarrota.

        Returns
        -------
        None or str
            None si se realiza correctamente o mensaje de error.
        """
        pass

    @abstractmethod
    def simular_movimientos(self) -> None:
        """
        Aplica cambios aleatorios a los precios de todas las acciones del mercado.

        Returns
        -------
        None
        """
        pass


class Mercado(BaseMercado):
    """Esta clase simulará un mercado financiero con un listado de acciones

    Attributes
    ----------
    nombre : str
        Nombre del mercado.
    _lista_acciones : list[Accion]
        Una lista de las acciones que hay en el mercado.
    _mercados_registrados : dict[str, Mercado]
        Un diccionario cuyas claves son los nombres de los mercados y los valores los mercados.

    Methods
    -------
    registrar_accion(accion: Accion)
        Sirve para añadir una acción al mercado
    obtener_precio(simbolo: str)
        Te da el precio de una acción dado su símbolo
    bancarrota(simbolo: str)
        Declara en bancarrota una acción dado su símbolo.
    simular_movimientos()
        Simula movimientos de un mercado (cambia precios aleatoriamente).
    __str__()
        Devuelve un string que da información sobre el mercado.
    __len__()
        Devuelve el número de acciones del mercado.
    __getitem__(item: int)
        Devuelve el elemento en la posición item de la lista de acciones
    __contains__(simbolo: str)
        Devuelve True si la acción con el simbolo pasado está en el mercado.
    __eq__(other: Mercado)
        Dos mercados son iguales si tienen las mismas acciones.
    __ne__(other: Mercado)
        Dos mercados no son iguales si no tienen las  mismas acciones.
    __add__(other: Mercado)
        Sumas dos mercados y el resultado es un mercado con las acciones de ambas.
    __iadd__(other: Mercado)
        Le sumas a un mercado las acciones del otro
    """
    _mercados_registrados: dict[str, "Mercado"] = {}

    def __init__(self, nombre: str, lista_acciones: list[Accion]):
        """
        Parameters
        ----------
        nombre : str
            Nombre del mercado.
        lista_acciones : list[Accion]
            Lista inicial de acciones que se registrarán en el mercado.

        Raises
        ------
        ValueError
            En el caso de que ya existe un mercado con el nombre que pasamos.
        ValueError
            No puede haber acciones repetidas en lista_acciones.
        TypeError
            En el caso de que algún objeto de lista_acciones no sea una acción, salta error.
        """
        if nombre in Mercado._mercados_registrados:
            raise ValueError(f"Ya existe un mercado con el nombre {nombre}")
        for i in range(len(lista_acciones)):
            accion = lista_acciones[i]
            if accion in lista_acciones[:i]:
                raise ValueError(f"No puede haber acciones repetidas")
            if not isinstance(accion, Accion):
                raise TypeError(f"El objeto {accion}, que es el término {i}, no pertenece a la clase Accion")

        self.nombre = nombre
        self._lista_acciones = lista_acciones
        Mercado._mercados_registrados[nombre] = self

    def registrar_accion(self, accion: Accion) -> None:
        """Este método sirve para registrar una nueva acción en el mercado

        Parameters
        ----------
        accion : Accion
            La acción que queremos registrar.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Nos da error si queremos añadir una acción que ya esté.
        TypeError
            En el caso de que acción no sea de Acción, salta error.
        """
        for a in self._lista_acciones:
            if a.simbolo == accion.simbolo:
                raise ValueError(f"La acción con símbolo {accion.simbolo} ya está registrada en el mercado.")

        if not isinstance(accion, Accion):
            raise TypeError(f'El objeto {accion} no pertenece a la clase Accion')
        self._lista_acciones.append(accion)

    def obtener_precio(self, simbolo: str) -> Union[float, str]:
        """Este método sirve para obtener el precio de una acción dado su símbolo

        Parameters
        ----------
        simbolo : str
            El símbolo de la acción de la que queremos obtener su precio.

        Returns
        -------
        Union[float,str]
            Nos devolverá el precio de la acción (el float) o un mensaje diciendo que no
            existen acciones en el mercado con ese símbolo (el str).
        """
        for accion in self._lista_acciones:
            if accion.simbolo == simbolo:
                return accion._precio_actual
        return "No existen acciones con este símbolo"

    def eliminar_accion(self, simbolo: str) -> None:
        """Este método sirve para eliminar una acción del mercado.

        Parameters
        ----------
        simbolo : str
            El símbolo de la acción que queremos eliminar.

        Returns
        -------
        None

        Raises
        ------
        ValueError
            Salta error si la acción que le hemos pasado no está en el mercado.
        """
        accion = Accion._acciones_registradas[simbolo]
        if accion not in self._lista_acciones:
            raise ValueError(f"La acción con el símbolo {simbolo} no está en el mercado {self.nombre}")
        self._lista_acciones.remove(accion)


    def bancarrota(self, simbolo: str) -> Optional[str]:
        """
        Este método sirve para declarar en bancarrota una acción dado su símbolo. Lo que
        hace es eliminarla de lista_acciones y actualiza su precio a 0.

        Parameters
        ----------
        simbolo : str
            El símbolo de la acción que queremos declarar en bancarrota.

        Returns
        -------
        Optional[str]
            Nos devolverá None si todo va bien y un str si la acción que hemos pasado ya estaba
            en bancarrota.
        """
        try:
            for accion in self._lista_acciones:
                if accion.simbolo == simbolo:
                    self._lista_acciones.remove(accion)
                    accion.actualizar_precio(0)  # al estar en bancarrota, su precio es 0
                    break
            else:  # no hemos hecho break en ningún momento, por lo que la acción no está en el merado
                return f"No se encontró la acción con símbolo {simbolo} en el mercado {self.nombre}"
        except ValueError:  # si el precio ya es 0 dará error al actualizar el precio
            return "Esa acción ya está en bancarrota"

    def simular_movimientos(self) -> None:
        """
        Este método sirve para simular movimientos en el mercado (cambia de precio
        aleatoriamente todas las acciones.)

        Returns
        -------
        None
        """
        for accion in self._lista_acciones:
            variacion = random.uniform(-0.05, 0.05)
            nuevo_precio = round(accion._precio_actual * (1 + variacion), 3)
            accion.actualizar_precio(nuevo_precio)

    def __str__(self) -> str:
        """
        Este método sirve para crear la forma de imprimir un mercado.

        Parameters
        ----------
        None

        Returns:
        str
            La forma de imprimir un mercado.
        """
        cantidad = len(self._lista_acciones)
        palabra = "acción registrada" if cantidad == 1 else "acciones registradas"
        return f"El mercado {self.nombre} tiene {cantidad} {palabra}."

    def __len__(self) -> int:
        """
        Este método sirve para definir la longitud de un mercado. Su longitud será la cantidad de
        acciones que tenga.

        Returns
        -------
        int
            La cantidad de acciones que tiene el mercado.
        """
        return len(self._lista_acciones)

    def __getitem__(self, item: int) -> Accion:
        """
        Este método sirve para definir el get item de un mercado. Al hacer mercado[item] se
        devolverá la acción que esté en la posición item de la lista de acciones.

        Parameters
        ----------
        item : int
            El índice de la acción que queremos de la lista de acciones.

        Returns
        -------
        Accion
            Se devuelve la acción que está en la posición item de la lista de acciones.
        """
        return self._lista_acciones[item]

    def __contains__(self, simbolo: str) -> bool:
        """
        Comprueba si una acción con el símbolo dado está registrada en el mercado. Al hacer
        simbolo in mercado se verá si la acción cuyo símbolo es simbolo está en el mercado.

        Parameters
        ----------
        simbolo : str
            El símbolo de la acción que queremos ver si está en la lista de acciones.

        Returns
        -------
        bool
            Se devuelve True si el símbolo de alguna de las acciones de la lista de acciones
            es simbolo y False si no hay.
        """
        for accion in self._lista_acciones:
            if accion.simbolo == simbolo:
                return True
        return False

    def __eq__(self, other: 'Mercado') -> bool:
        """
        Este método sirve para definir cuándo dos métodos son iguales. Serán iguales si
        tienen las mismas acciones.

        Parameters
        ----------
        other : Mercado
            El mercado que compararemos con el self.

        Returns
        -------
        bool
            Se devuelve True si ambos mercados tienen las mismas acciones y False si no.
        """
        return set(self._lista_acciones) == set(other._lista_acciones)

    def __ne__(self, other: 'Mercado') -> bool:
        """
        Este método sirve para definir cuándo dos métodos no son iguales. Serán iguales si
        tienen las mismas acciones.

        Parameters
        ----------
        other : Mercado
            El mercado que compararemos con el self.

        Returns
        -------
        bool
            Se devuelve False si ambos mercados tienen las mismas acciones y True si no.
        """
        return set(self._lista_acciones) != set(other._lista_acciones)

    def __add__(self, other: 'Mercado') -> 'Mercado':
        """
        Este método sirve para definir la suma entre dos mercados. Lo que se hace es
        hacer una combinación de los nombres y juntar en una lista las listas de acciones
        de ambos mercados.

        Parameters
        ----------
        other : Mercado
            El mercado que sumaremos con el self.

        Returns
        -------
        Mercado
            El resultado de la suma.

        Raises
        ------
        ValueError
            Ocurre cuando el nombre del mercado resultante ya existe.
        """
        nombre = self.nombre + '_' + other.nombre
        if nombre in Mercado._mercados_registrados:
            raise ValueError(f"Ya existe un mercado con el nombre combinado {nombre}")
        distintas = [accion for accion in other._lista_acciones if accion not in self._lista_acciones]
        lista_acciones = self._lista_acciones + distintas
        return Mercado(nombre, lista_acciones)

    def __iadd__(self, other: 'Mercado') -> 'Mercado':
        """
        Este método sirve para definir mercado1 += mercado2. Lo que se hace es que a mercado1
        se le añaden las acciones de la lista de acciones de mercado2

        Parameters
        ----------
        other : Mercado
            El mercado que sumaremos con el self.

        Returns
        -------
        Mercado
            El self con su lista de acciones actualizada.
        """
        distintas = [accion for accion in other._lista_acciones if accion not in self._lista_acciones]
        self._lista_acciones += distintas
        return self