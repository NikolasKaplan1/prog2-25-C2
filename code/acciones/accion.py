from datetime import date

class Accion:
    """
    La clase Accion sirve para crear una nueva acción.
    Atributos
    -------------
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
        """
        
        self.simbolo = simbolo
        self.nombre = nombre
        self.precio_actual = precio_actual
        self.historial_precios = historial_precios
    def actualizar_precio(self,nuevo_precio: float):
        """Este método sirve para actualizar el precio actual de una acción. Además de ello,
        se actualizará el historial de precios añadiendo el precio nuevo y la fecha de hoy
        Parámetros
        ---------------
        nuevo_precio: float
            El precio que queremos que tenga la acción.
        """
        
        self.historial_precios[date.today()] = nuevo_precio
        self.precio_actual = nuevo_precio
    def __str__(self):
        """Este método devuelve una representación de una acción con todos sus datos en formato texto."""

        print(f"El logo de la acción de la empresa {self.nombre} es {self.precio_actual} y el precio actual de dicha acción es {self.precio_actual}. El historial de precios es ", end = '')
        for key, value in self.historial_precios.items():
            print(f"{key}: {value}", end = '')

