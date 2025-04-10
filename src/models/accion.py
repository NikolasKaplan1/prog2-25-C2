import yfinance as yf
#Esta librería es para añadir una librería novedosa. Sirve para crear acciones con datos reales
from datetime import date

class Accion:
    """
    La clase Accion representa una acción de una empresa.

    Atributos
    ---------------
    acciones_registradas: dict[str, Accion]
        Un atributo de clase que sirve para almacenar las acciones registradas
    simbolo: str
        El símbolo de la acción (e.g., "AAPL" para Apple).
    
    nombre: str
        El nombre de la acción (e.g., "Apple Inc.").

    precio_actual: float
        El precio actual de la acción.
    
    historial_precios: dict[str, float]
        Un diccionario donde las claves son las fechas y los valores son los precios de la acción en esas fechas.
    
    Métodos
    ---------------
    actualizar_precio(nuevo_precio: float):
        Actualiza el precio de la acción y agrega la fecha de la actualización al historial.

    obtener_precio():
        Devuelve el precio actual de la acción.

    __str__():
        Devuelve una representación en texto de la acción con su nombre, símbolo y precio actual.
    """

    acciones_registradas: dict[str, 'Accion'] = {}
    def __init__(self, simbolo: str, nombre: str, precio_actual: float, historial_precios: dict[str, float]): #el str sería la fecha y el float el valor de la acción en esa fecha
        """
        Inicializa una nueva acción.

        Parámetros:
        ---------------
        simbolo (str): El símbolo de la acción.
        nombre (str): El nombre de la acción.
        precio_actual (float): El precio actual de la acción.
        historial_precios (dict): Un diccionario con el historial de precios de la acción.
        
        """
        self.simbolo = simbolo
        self.nombre = nombre
        self.precio_actual = precio_actual
        self.historial_precios = historial_precios
        Accion.acciones_registradas[simbolo] = self

    def actualizar_precio(self, nuevo_precio: float):
        """
        Actualiza el precio actual de la acción y agrega la fecha de la actualización al historial.

        Parámetros:
        ---------------
        nuevo_precio (float): El nuevo precio de la acción.
        """
        self.historial_precios[str(date.today())] = nuevo_precio
        self.precio_actual = nuevo_precio

    def obtener_precio(self):
        """
        Devuelve el precio actual de la acción.

        Retorna:
        ---------------
        float: El precio actual de la acción.
        """
        return self.precio_actual

    def __str__(self):
        """
        Devuelve una representación en texto de la acción con su nombre, símbolo y precio actual.

        Retorna:
        ---------------
        str: Una cadena con la representación de la acción.
        """
        cadena = f"El símbolo de la acción de la empresa {self.nombre} es {self.simbolo} y el precio actual de dicha acción es {self.precio_actual}. "
        cadena += "El historial de precios es: "
        for key, value in self.historial_precios.items():
            cadena += f"{key}: {value} "
        return cadena


class AccionReal(Accion):
    """
    La clase AccionReal extiende la clase Accion y obtiene los datos de la acción en tiempo real utilizando Yahoo Finance.

    Métodos
    ---------------
    actualizar_precio():
        Actualiza el precio actual obteniéndolo desde Yahoo Finance.
    """

    def __init__(self, simbolo: str):
        """
        Inicializa una instancia de AccionReal obteniendo los datos de la acción desde Yahoo Finance.

        Parámetros:
        ---------------
        simbolo (str): El símbolo de la acción.

        Raises:
        ---------------
        ValueError 
            Si no se encuentran datos de la acción en el último año en Yahoo Finance.
        """
        # Obtenemos la representación de la acción con su símbolo.
        repr = yf.Ticker(simbolo) 
        data = repr.history(period="365d")  # Datos de los últimos 365 días

        if data.empty:
            raise ValueError(f"No se encontraron datos para la acción con el símbolo {simbolo} en el último año.")

        # Historial de precios: fecha como clave y precio de cierre como valor.
        historial = {}
        for index, row in data.iterrows():
            historial[str(index.date())] = round(row['Close'], 2)

        # El precio actual es el precio de cierre del último día.
        precio_actual = round(data.iloc[-1]['Close'], 2)
        nombre = repr.info.get("shortName", simbolo)

        super().__init__(simbolo, nombre, precio_actual, historial)

    def actualizar_precio(self):
        """
        Actualiza el precio de la acción obteniéndolo desde Yahoo Finance.

        Raises:
        ---------------
        ValueError: Si no se pueden obtener datos de la acción en el último día desde Yahoo Finance.
        """
        ticker = yf.Ticker(self.simbolo)
        data = ticker.history(period="1d")

        if data.empty:
            raise ValueError(f"No se puede actualizar el precio de {self.simbolo}")
        
        nuevo_precio = round(data['Close'][-1], 2)
        self.precio_actual = nuevo_precio
        self.historial_precios[str(date.today())] = nuevo_precio

