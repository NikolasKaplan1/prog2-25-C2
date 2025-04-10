import yfinance as yf
#Esta librería es para añadir una librería novedosa. Sirve para crear acciones con datos reales
from datetime import date
class Accion:
    """
    La clase Accion sirve para crear una nueva acción.
    
    Atributos
    -------------
    acciones_registradas: dict[str, Accion]
        Un atributo de clase que sirve para almacenar las acciones registradas
    simbolo: str
        Un string que es el símbolo de la acción
    nombre: str
        El nombre de la acción
    precio_actual: float
        El precio actual de la accion
    historial_precios: dict[str,float]
        Te da el historial de precios de esa accion
    
    Métodos
    -------------
    actualizar_precio(nuevo_precio)
        Permite actualizar el precio actual de una acción.
    obtener_precio(simbolo)
        Dado el símbolo de la acción, te da su precio.
    __str__():
        Devuelve una representación de una acción con todos sus datos en formato texto.
    """

    acciones_registradas: dict[str, Accion] = {}
    def __init__(self, simbolo: str, nombre: str, precio_actual: float, historial_precios: dict[str, float]): #el str sería la fecha y el float el valor de la acción en esa fecha
        """
        Parámetros
        ---------------
        simbolo: str
            El simbolo de la accion
        nombre: str
            El nombre de la acción
        precio_actual: float
            El precio actual de la accion
        historial_precios: dict[str,float]
            Te da el historial de precios de esa accion en forma de diccionario.
            Las claves (strings) son la fecha en la que la acción comenzó a tener 
            ese precio y los valores los precios antiguos (floats)
        
        Raises
        -------------
        ValueError:
            Da error si ya existe una acción con el símbolo que hemos pasado
        """
        if simbolo in acciones_registradas:
            raise ValueError(f"Ya existe una acción con el símbolo {simbolo}")
        self.simbolo = simbolo
        self.nombre = nombre
        self.precio_actual = precio_actual
        self.historial_precios = historial_precios
        Accion.acciones_registradas[simbolo] = self
  
    def actualizar_precio(self,nuevo_precio: float):
        """Este método sirve para actualizar el precio actual de una acción. Además de ello,
        se actualizará el historial de precios añadiendo el precio nuevo y la fecha de hoy
        
        Parámetros
        ---------------
        nuevo_precio: float
            El precio que queremos que tenga la acción.
        """
        self.historial_precios[str(date.today())] = nuevo_precio
        self.precio_actual = nuevo_precio

    def __str__(self):
        """Este método devuelve una representación de una acción con todos sus datos en formato texto."""
        cadena = f"El símboll de la acción de la empresa {self.nombre} es {self.simbolo} y el precio actual de dicha acción es {self.precio_actual}. El historial de precios es "
        for key, value in self.historial_precios.items():
            cadena += f"{key}: {value}"
        return cadena


class AccionReal(Accion):
    """
    Clase AccionReal que extiende Accion y obtiene los datos reales usando yfinance.
    """

    def __init__(self, simbolo: str):
        """
        Crea una instancia de AccionReal obteniendo datos desde Yahoo Finance.

        Parámetros
        ----------------
        simbolo: str
            Símbolo de la acción.

        Raises
        -------------
        ValueError
            No hay datos de la acción dada en este último año.
        """
        repr = yf.Ticker(simbolo) #esto da una representación de la acción real con su símbolo
        data = repr.history(period="365d") #nos da los datos del último año
        if data.empty:
            raise ValueError(f"No se encontraron datos para la acción con el símbolo {simbolo} en este último año")

        historial = {}
        for index, row in data.iterrows():
            historial[str(index.date())] = round(row['Close'],2)
            #se utiliza index.date() porque el índice es fecha y hora y a nosotros solo nos interesa la fecha.
            #Luego se pasa a str porque trabajamos así con él.
        precio_actual = round(data.iloc[-1]['Close'], 2) #el precio actual, es el precio de cierre del último día.
        nombre = repr.info.get("shortName", simbolo)

        super().__init__(simbolo, nombre, precio_actual, historial)

    def actualizar_precio(self):
        """
        Actualiza el precio actual obteniéndolo desde Yahoo Finance.

        Raises
        -------------
        ValueError
            No hay datos de la acción dada en este último día.
        """
        ticker = yf.Ticker(self.simbolo)
        data = ticker.history(period="1d")
        if data.empty:
            raise ValueError(f"No se puede actualizar el precio de {self.simbolo}")
    
        nuevo_precio = round(data['Close'][-1], 2)
        super().actualizar_precio(nuevo_precio)
