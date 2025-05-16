from models.accion import Accion, AccionReal
from models.mercado import Mercado
from models.transaccion import Transaccion
from models.inversor import Inversor
from estrategias import InversorAgresivo, InversorConservador, IA
from typing import Union
import random
import yfinance as yf

from routers.manejo_archivos import (
    exportar_transacciones_csv,
    exportar_inversores_pickle,
    exportar_acciones_csv,
    exportar_historial_precios_csv,
    exportar_acciones_pickle,
    exportar_historiales_pickle,
    exportar_acciones_reales_csv,
    exportar_mercados_csv,
    exportar_mercados_registrados_pickle,
    acciones_por_mercado_csv
)
from src.models import mercado


# Clases Accion y AccionReal
def crear_accion(simbolo: str, nombre: str, precio_actual: float, historial_precios: dict[str, float]) -> dict[
    str, str]:
    """
    Esta función crea una nueva acción.

    Parameters
    ----------
    simbolo : str
        El símbolo de la acción.
    nombre : str
        El nombre de la acción.
    precio_actual : float
        El precio actual de la acción.
    historial_precios : dict
        Un diccionario con el historial de precios de la acción.

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o éxito.

    Raises
    ------
    Error
        Nos dará error si ya existe una acción con el símbolo que le pasamos.
    """
    if simbolo in Accion._acciones_registradas:
        return {"error": f"Ya existe una acción con el símbolo {simbolo}"}
    Accion(simbolo, nombre, precio_actual, historial_precios)
    exportar_acciones_csv()
    exportar_historial_precios_csv()
    exportar_acciones_pickle()
    exportar_historiales_pickle()
    return {"mensaje": "Acción añadida correctamente"}


def crear_accion_real(simbolo: str) -> dict[str, str]:
    """
    Esta función crea una nueva acción con datos de la vida real.

    Parameters
    ----------
    simbolo : str
        El símbolo de la acción.

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o éxito.

    Raises
    ------
    Error
        Nos dará error si no se han encontrado datos reales para la acción que le hemos pasado.
    Error
        Nos dará error si ya existe una acción con el símbolo que le pasamos.
    """
    repr = yf.Ticker(simbolo)  # esto da una representación de la acción real con su símbolo
    data = repr.history(period="365d")  # nos da los datos del último año
    if data.empty:
        return {"error": f"No se encontraron datos para la acción con el símbolo {simbolo} en este último año"}
    if simbolo in Accion._acciones_registradas:
        return {"error": f"Ya existe una acción con el símbolo {simbolo}"}
    AccionReal(simbolo)
    exportar_acciones_csv()
    exportar_historial_precios_csv()
    exportar_acciones_pickle()
    exportar_historiales_pickle()
    exportar_acciones_reales_csv()
    return {"mensaje": "Acción añadida correctamente"}


def actualizar_precio(simbolo: str, nuevo_precio: float) -> dict[str, str]:
    """
    Esta función actualiza el precio de una acción dada.

    Parameters
    ----------
    simbolo : str
        El símbolo de la acción.
    nuevo_precio : float
        El nuevo precio que le queremos poner a la acción.

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o éxito.

    Raises
    ------
    Error
        Nos dará error si no existe una acción con el símbolo que le pasamos.
    ValueError
        Nos dará error si el precio nuevo que hemos puesto es el actual.
    """
    if simbolo not in Accion._acciones_registradas:
        return {"error": f"No existe una acción con el símbolo {simbolo}"}
    Accion._acciones_registradas[simbolo].actualizar_precio(nuevo_precio)
    return {"mensaje": "Precio actualizado correctamente"}
    try:
        Accion._acciones_registradas[simbolo].actualizar_precio(nuevo_precio)
        exportar_acciones_csv()
        exportar_historial_precios_csv()
        exportar_acciones_pickle()
        exportar_historiales_pickle()
        return {"mensaje": "Precio actualizado correctamente"}
    except ValueError:
        return {"error": "El precio que has puesto es el actual"}


def actualizar_precio_real(simbolo: str) -> dict[str, str]:
    """
    Esta función actualiza el precio de una acción dada con su precio en la vida real.

    Parameters
    ----------
    simbolo : str
        El símbolo de la acción.

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o éxito.

    Raises
    ------
    Error
        Nos dará error si no existe una acción con el símbolo que le pasamos.
    Error
        Nos dará error si no existe una acción en la vida real con el símbolo que pasamos.
    """
    if simbolo not in Accion._acciones_registradas:
        return {"error": f"No existe una acción con el símbolo {simbolo}"}
    accion = Accion._acciones_registradas[simbolo]
    if type(accion) is not AccionReal:
        return {"error": f"La acción con el símbolo {simbolo} no es una acción real"}
    try:
        accion.actualizar_precio_real()
        exportar_acciones_csv()
        exportar_historial_precios_csv()
        exportar_acciones_pickle()
        exportar_historiales_pickle()
        exportar_acciones_reales_csv()
        return {"mensaje": "Precio actualizado correctamente"}
    except ValueError:
        return {"error": f"No se puede actualizar el precio de {simbolo} ya que no hay datos en Yahoo Finance"}


def datos_accion(simbolo: str) -> dict[str, str]:
    """
    Esta función nos devuelve los datos de la acción que le pasamos.

    Parameters
    ----------
    simbolo : str
        El símbolo de la acción.

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o los datos de la acción que le pasamos.

    Raises
    ------
    Error
        Nos dará error si no existe una acción con el símbolo que le pasamos.
    """
    if simbolo not in Accion._acciones_registradas:
        return {"error": f"No existe una acción con el símbolo {simbolo}"}
    accion = Accion._acciones_registradas[simbolo]
    return {"mensaje": str(accion)}


def menor_que(simbolo1: str, simbolo2: str) -> dict[str, str]:
    """
    Esta función sirve para comparar si una acción es menor a otra en base a su precio.

    Parameters
    ----------
    simbolo1 : str
        El símbolo de la primera acción.
    simbolo2 : str
        El símbolo de la segunda acción.

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o los datos de la acción que le pasamos.

    Raises
    ------
    Error
        Nos dará error si no existe una acción con alguno de los símbolos que le pasamos.
    """
    if simbolo1 not in Accion._acciones_registradas:
        return {"error": f"No existe una acción con el símbolo {simbolo1}"}
    if simbolo2 not in Accion._acciones_registradas:
        return {"error": f"No existe una acción con el símbolo {simbolo2}"}
    accion1 = Accion._acciones_registradas[simbolo1]
    accion2 = Accion._acciones_registradas[simbolo2]
    resultado = accion1 < accion2
    if resultado:
        return {"mensaje": f"El precio de {simbolo1} es menor que el de {simbolo2}"}
    else:
        return {"mensaje": f"El precio de {simbolo1} no es menor que el de {simbolo2}"}


def mayor_que(simbolo1: str, simbolo2: str) -> dict[str, str]:
    """
    Esta función sirve para comparar si una acción es mayor a otra en base a su precio.

    Parameters
    ----------
    simbolo1 : str
        El símbolo de la primera acción.
    simbolo2 : str
        El símbolo de la segunda acción.

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o los datos de la acción que le pasamos.

    Raises
    ------
    Error
        Nos dará error si no existe una acción con alguno de los símbolos que le pasamos.
    """
    if simbolo1 not in Accion._acciones_registradas:
        return {"error": f"No existe una acción con el símbolo {simbolo1}"}
    if simbolo2 not in Accion._acciones_registradas:
        return {"error": f"No existe una acción con el símbolo {simbolo2}"}
    accion1 = Accion._acciones_registradas[simbolo1]
    accion2 = Accion._acciones_registradas[simbolo2]
    resultado = accion1 > accion2
    if resultado:
        return {"mensaje": f"El precio de {simbolo1} es mayor que {simbolo2}"}
    else:
        return {"mensaje": f"El precio de {simbolo1} no es mayor que {simbolo2}"}


# Clase Inversor

inversores_registrados = {}


def crea_inversor(nombre: str, capital: float, tipo: str) -> dict[str, str]:
    """
    Esta función crea un inversor nuevo y lo guarda en el diccionario de inversores.

    Parameters
    ----------
    nombre : str
        Nombre del inversor.
    capital : float
        Capital del inversor
    tipo : str
        Tipo de inversor ("Agresivo" ó "Pasivo").

    Returns
    -------
    dict[str, str]
        Diccionario con un mensaje de éxito.

    Raises
    ------
    Error
        Si el tipo de inversor no es válido o ya ha sido registrado el inversor.
    """
    if nombre in inversores_registrados:
        return {"error": f"Ya existe un inversor bajo el nombre: {nombre}"}
    if tipo == "Agresivo":
        inversores_registrados[nombre] = InversorAgresivo(nombre, capital)
    elif tipo == "Pasivo":
        inversores_registrados[nombre] = InversorConservador(nombre, capital)
    else:
        return {"error": "Tipo de inversor no válido."}
    exportar_inversores_pickle(list(inversores_registrados.values()))
    return {"mensaje": f"Inversor {nombre} creado exitosamente como {tipo}"}


def datos_inversor(nombre: str) -> dict[str, Union[str, float]]:
    """
    Devuelve el capital del inversor y el tipo que es.

    Parameters
    ----------
    nombre : str
        Nombre del inversor

    Returns
    -------
    dict[str, Union[str, float]]
        Diccionario con información del inversor.

    Raises
    ------
    Error
        Si el inversor no ha sido registrado previamente.

    """
    if nombre not in inversores_registrados:
        return {"error": f"El inversor '{nombre}' no está registrado"}

    inversor = inversores_registrados[nombre]
    if isinstance(inversor, InversorAgresivo):
        tipo = "Agresivo"
    else:
        tipo = "Pasivo"
    return {"nombre": nombre,
            "capital": round(inversor.capital, 2),
            "tipo": tipo
            }


def mostrar_cartera(nombre: str) -> dict[str, str]:
    """
    Muestra el contenido de la cartera de un inversor.

    Parameters
    ----------
    nombre : str
        Nombre del inversor.

    Returns
    -------
    dict[str, str]
        Diccionario con el resumen de la cartera.

    Raises
    ------
    Error
        Si el inversor no ha sido registrado previamente.
    """
    if nombre not in inversores_registrados:
        return {"error": f"El inversor '{nombre}' no está registrado"}
    inversor = inversores_registrados[nombre]
    return {"mensaje": inversor.mostrar_cartera()}


def comprar_accion(nombre: str, simbolo: str, cantidad: int) -> dict[str, str]:
    """
    Ejecuta la compra de una accion para un inversor.

    Parameters
    ----------
    nombre : str
        nombre del inversor.
    simbolo : str
        simbolo de la accion.
    cantidad : int
        numero de acciones a comprar.

    Returns
    -------
    dict[str, str]
        Resultado de la operación.

    Raises
    ------
    Error
        Si el inversor no está registrado.
    Error
        Si la acción con el símbolo introducido no existe.
    """
    if nombre not in inversores_registrados:
        return {"error": f"El inversor '{nombre}' no está registrado"}
    inversor = inversores_registrados[nombre]
    if simbolo not in Accion._acciones_registradas:
        return {"error": f"La acción con el símbolo {simbolo} no existe"}
    accion = Accion._acciones_registradas[simbolo]
    try:
        inversor.comprar(accion, cantidad)
        return {"mensaje": f"{nombre} ha comprado {cantidad} acciones de {accion.nombre} exitosamente"}
    except ValueError as e:
        return {"error": str(e)}


def vender_accion(nombre: str, simbolo: str, cantidad: int) -> dict[str, str]:
    """
    Ejecuta la venta de una accion para un inversor.

    Parameters
    ----------
    nombre : str
        nombre del inversor.
    simbolo : str
        simbolo de la accion.
    cantidad : int
        numero de acciones a comprar.

    Returns
    -------
    dict[str, str]
        Resultado de la operación.

    Raises
    ------
    Error
        Si el inversor no está registrado.
    Error
        Si la acción con el símbolo introducido no existe.
    """
    if nombre not in inversores_registrados:
        return {"error": f"El inversor '{nombre}' no está registrado"}
    inversor = inversores_registrados[nombre]
    if simbolo not in Accion._acciones_registradas:
        return {"error": f"La acción con el símbolo {simbolo} no existe"}
    accion = Accion._acciones_registradas[simbolo]
    try:
        inversor.vender(accion, cantidad)
        return {"mensaje": f"{nombre} ha vendido {cantidad} acciones de {accion.nombre} exitosamente"}
    except ValueError as e:
        return {"error": str(e)}


def mostrar_transaccion_registrada(nombre: str) -> dict[str, str]:
    """
    Muestra todas las transacciones realizdas por un inversor.

    Parameters
    ----------
    nombre : str
        Nombre del inversor registrado.

    Returns
    -------
    dict[str, str]
        Mensaje con resumen de las transacciones.

    Raises
    ------
    Error
        Si el inversor no está registrado.
    Error
        Si el inversor no ha realizado ninguna operación.

    """
    if nombre not in inversores_registrados:
        return {"error": f"El inversor '{nombre}' no está registrado"}
    inversor = inversores_registrados[nombre]
    if not inversor._transacciones:
        return {"mensaje": "Este inversor no ha realizado ninguna transacción."}
    resumen_transacciones = f"Historial de transacciones de {nombre}:\n"
    for transaccion in inversor._transacciones:
        resumen_transacciones += str(transaccion) + "\n"
    return {"mensaje": resumen_transacciones}


# Utiliza la sobrecarga del operador + para comprar acciones
def comprar_acciones_con_operador(nombre: str, simbolo: str, cantidad: int) -> dict[str, str]:
    """
    Realiza una compra de acciones usando la sobrecarga del operador `+`.

    Parameters
    ----------
    nombre : str
        Nombre del inversor.
    simbolo : str
        Símbolo de la acción.
    cantidad : int
        Cantidad de acciones.

    Returns
    -------
    dict[str, str]
        Resultado de la operación.
    """
    if nombre not in inversores_registrados:
        return {"error": f"El inversor '{nombre}' no está registrado"}

    inversor = inversores_registrados[nombre]
    if simbolo not in Accion._acciones_registradas:
        return {"error": f"La acción con el símbolo {simbolo} no existe"}
    accion = Accion._acciones_registradas[simbolo]
    try:
        inversor + (accion, cantidad)
        return {"mensaje": f"{nombre} ha comprado {cantidad} acciones de {accion.nombre} usando el operador '+'."}
    except Exception as e:
        return {"error": str(e)}


def vender_acciones_con_operador(nombre: str, simbolo: str, cantidad: int) -> dict[str, str]:
    """
    Realiza una compra de acciones usando la sobrecarga del operador `-`.

    Parameters
    ----------
    nombre : str
        Nombre del inversor.
    simbolo : str
        Símbolo de la acción.
    cantidad : int
        Cantidad de acciones.

    Returns
    -------
    dict[str, str]
        Resultado de la operación.
    """
    if nombre not in inversores_registrados:
        return {"error": f"El inversor '{nombre}' no está registrado"}

    inversor = inversores_registrados[nombre]
    if simbolo not in Accion._acciones_registradas:
        return {"error": f"La acción con el símbolo {simbolo} no existe"}
    accion = Accion._acciones_registradas[simbolo]
    try:
        inversor - (accion, cantidad)
        return {"mensaje": f"{nombre} ha vendido {cantidad} acciones de {accion.nombre} usando el operador '-'."}
    except Exception as e:
        return {"error": str(e)}


def inversor_contiene_accion(nombre: str, simbolo: str) -> dict[str, str]:
    """
    Verifica si un inversor tiene una accion específica usando la sobrecarga del operador 'in'.

    Parameters
    ----------
    nombre : str
        Nombre del inversor.
    simbolo : str
        Simbolo de la acción.

    Returns
    -------
    dict[str, str]
        Mensaje indicando si el símbolo está o no en la cartera del inversor.

    Raises
    ------
    Error
        Si el inversor no está registrado
    """
    if nombre not in inversores_registrados:
        return {"error": f"El inversor '{nombre} no está registrado"}
    if simbolo in inversores_registrados[nombre]:
        return {"mensaje": f"El inversor {nombre} tiene acciones de {simbolo}."}
    return {"mensaje": f"El inversor {nombre} NO tiene acciones de {simbolo}."}


def comparar_inversores(nombre1: str, nombre2: str) -> dict[str, str]:
    """
    Compara dos inversores por su cartera usando la sobrecarga del operador `==`.

    Parameters
    ----------
    nombre1 : str
        Nombre del primer inversor.
    nombre2 : str
        Nombre del segundo inversor.

    Returns
    -------
    dict[str, str]
        Resultado de la comparación.
    """
    if nombre1 not in inversores_registrados or nombre2 not in inversores_registrados:
        return {"error": "Ambos inversores no están registrados. No se puede realizar la comparación."}

    if inversores_registrados[nombre1] == inversores_registrados[nombre2]:
        return {"mensaje": f"{nombre1} y {nombre2} han invertido en las mismas empresas."}
    else:
        return {"mensaje": f"{nombre1} y {nombre2} NO han invertido en las mismas empresas."}


# Clase Mercado
def crear_mercado(nombre: str, lista_acciones: list[str]) -> dict[str, str]:
    """
    Esta función crea un mercado financiero.

    Parameters
    ----------
    nombre : str
        Nombre del mercado
    lista_acciones : list[str]
        Es una lista en la que se encuentran los símbolos de todas las acciones disponibles
        en el mercado

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o éxito.

    Raises
    ------
    Error
        Da error si ya existe un mercado con el nombre que le pasamos.
    Error
        Da error si hay acciones repetidas.
    Error
        Da error si hay algún símbolo de los que le pasamos que no está asociado a ninguna acción
    """
    if nombre in Mercado._mercados_registrados:
        return {"error": f"Ya existe un mercado con el nombre {nombre}"}
    for i in range(len(lista_acciones)):
        simbolo = lista_acciones[i]
        if simbolo in lista_acciones[:i]:
            return {"error": f"No puede haber acciones repetidas. Se repite {simbolo}"}
        if simbolo not in Accion._acciones_registradas:
            return {"error": f"El símbolo {simbolo} que es el término {i}, no está asociado a ninguna acción existente"}
        lista_acciones[i] = Accion._acciones_registradas[simbolo]
    Mercado(nombre, lista_acciones)
    exportar_mercados_csv()
    acciones_por_mercado_csv()
    exportar_mercados_registrados_pickle()
    return {"mensaje": "Mercado creado correctamente"}


def datos_mercado(nombre: str) -> dict[str, str]:
    """
    Esta función sirve para imprimir los datos del mercado con el nombre que le pasamos.

    Parameters
    ----------
    nombre : str
        Nombre del mercado

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o la impresión del mercado.

    Raises
    ------
    Error
        Da error si no existe un mercado con el nombre que le pasamos.
    """
    if nombre not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre}"}
    return {"mensaje": Mercado._mercados_registrados[nombre].__str__()}


def registrar_accion(nombre: str, simbolo: str) -> dict[str, str]:
    """
    Esta función registra una acción en el mercado que queremos

    Parameters
    ----------
    nombre : str
        Nombre del mercado
    simbolo : str
        Símbolo de la acción que queremos registrar al mercado.

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o éxito.

    Raises
    ------
    Error
        Da error si el símbolo que le pasamos no está asociado a ninguna acción
    Error
        Da error si no existe un mercado con el nombre que le pasamos.
    Error
        Da error si la acción que le pasamos ya está en el mercado.
    """
    if simbolo not in Accion._acciones_registradas:
        return {"error": f"No existe ninguna acción con el símbolo {simbolo}"}
    if nombre not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre}"}
    accion = Accion._acciones_registradas[simbolo]
    if accion in Mercado._mercados_registrados[nombre]._lista_acciones:
        return {"error": f"La acción con el símbolo {simbolo} ya está en el mercado {nombre}"}
    Mercado._mercados_registrados[nombre].registrar_accion(accion)
    exportar_mercados_csv()
    acciones_por_mercado_csv()
    exportar_mercados_registrados_pickle()
    return {"mensaje": "Acción registrada correctamente"}


def obtener_precio(nombre: str, simbolo: str) -> Union[dict[str, str], dict[str, float]]:
    """
    Con esta función obtenemos el precio de una acción dado el mercado en el que está y el símbolo de la acción.

    Parameters
    ----------
    nombre : str
        Nombre del mercado
    simbolo : str
        Símbolo de la acción de la que queremos obtener el precio.

    Returns
    -------
    Union[dict[str,str], dict[str,float]]
        Nos devolverá el precio de la acción (el dict[str,float]) o un mensaje de error
        (el dict[str,str]).

    Raises
    ------
    Error
        Da error si no existe un mercado con el nombre que le pasamos.
    Error
        Da error si el símbolo que le pasamos no está asociado a ninguna acción del mercado
        (este error se ve en el propio método de la clase Mercado, no se hace aquí)
    """
    if nombre not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre}"}
    mercado = Mercado._mercados_registrados[nombre]
    resultado = mercado.obtener_precio(simbolo)
    if isinstance(resultado, float):
        return {"precio": resultado}
    else:
        return {"error": resultado}

def eliminar_accion(nombre: str, simbolo: str) -> dict[str, str]:
    """
    Esta función sirve para eliminar una acción del mercado.

    Parameters
    ----------
    nombre : str
        Nombre del mercado
    simbolo : str
        El símbolo de la acción que queremos eliminar.

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o éxito.


    Raises
    ------
    Error
        Da error si no existe un mercado con el nombre que le pasamos.
    Error
        Da error si el símbolo que le pasamos no está asociado a ninguna acción del mercado.
    Error
        Da error si el simbolo de la acción que le pasamos no está en el mercado.
    """
    if nombre not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre}"}
    if simbolo not in Accion._acciones_registradas:
        return {"error": f"No existe una acción con el símbolo {simbolo}"}
    try:
        mercado = Mercado._mercados_registrados[nombre]
        mercado.eliminar_accion(simbolo)
        return {"mensaje": f"La acción {simbolo} se ha eliminado correctamente de {nombre}."}
    except ValuError:
        return {"error": f"La acción con el símbolo {simbolo} no está en el mercado {self.nombre}"}

def bancarrota(nombre: str, simbolo: str) -> dict[str, str]:
    """
    Esta función sirve para declarar en bancarrota una acción dado su símbolo. Lo que
    hace es eliminarla de lista_acciones y actualiza su precio a 0.

    Parameters
    ----------
    nombre : str
        Nombre del mercado
    simbolo : str
        Símbolo de la acción que queremos declarar en bancarrota.

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o éxito.

    Raises
    ------
    Error
        Da error si no existe un mercado con el nombre que le pasamos.
    Error
        Da error si el símbolo que le pasamos no está asociado a ninguna acción del mercado.
    Error
        Da error si la acción que queremos declarar en bancarrota ya lo está.
    """
    if nombre not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre}"}
    mercado = Mercado._mercados_registrados[nombre]
    resultado = mercado.bancarrota(simbolo)
    if resultado is None:
        exportar_mercados_csv()
        acciones_por_mercado_csv()
        exportar_mercados_registrados_pickle()
        exportar_acciones_csv()
        exportar_historial_precios_csv()
        exportar_acciones_pickle()
        exportar_historiales_pickle()
        if simbolo in AccionReal._acciones_reales_registradas:
            exportar_acciones_reales_csv()
        return {"mensaje": f"La empresa con símbolo {simbolo} se ha declarado en bancarrota exitosamente"}
    else:
        return {"error": resultado}


def simular_movimientos(nombre: str) -> dict[str, str]:
    """
    Esta función sirve para simular movimientos en un mercado.

    Parameters
    ----------
    nombre : str
        Nombre del mercado

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o éxito.

    Raises
    ------
    Error
        Da error si no existe un mercado con el nombre que le pasamos.
    """
    if nombre not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre}"}
    mercado = Mercado._mercados_registrados[nombre]
    mercado.simular_movimientos()
    return {"mensaje": "Movimiento simulado exitosamente"}


def tamaño(nombre: str) -> dict[str, str]:
    """
    Esta función devuelve el tamaño de un mercado en base al número de acciones que contiene.

    Parameters
    ----------
    nombre : str
        Nombre del mercado

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o la longitud del mercado.

    Raises
    ------
    Error
        Da error si no existe un mercado con el nombre que le pasamos.
    """
    if nombre not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre}"}
    mercado = Mercado._mercados_registrados[nombre]
    return {"mensaje": f"El tamaño del mercado es {len(mercado)}"}


def obtener_accion(nombre: str, item: int) -> dict[str, str]:
    """
    Esta función sirve para obtener la acción de un mercado dado un item.

    Parameters
    ----------
    nombre : str
        Nombre del mercado.
    item : int
        Posición de la acción en la lista de acciones del mercado.

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o el símbolo de la acción que estamos buscando.

    Raises
    ------
    Error
        Da error si no existe un mercado con el nombre que le pasamos.
    Error
        Da error si item no es un entero.
    Error
        Da error si el item no está en el rango posible.
    """
    if nombre not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre}"}
    mercado = Mercado._mercados_registrados[nombre]
    if not isinstance(item, int):
        return {"error": f"El parámetro {item} ha de ser un entero"}
    if not 0 <= item < len(mercado):
        return {"error": f"El parámetro {item} no está entre 0 y {len(mercado)}"}
    return {"mensaje": f"La acción que está en la posición {item} es {mercado[item].simbolo}"}


def contener(nombre: str, simbolo: str) -> dict[str, str]:
    """
    Esta función sirve para ver si una acción está contenida en un mercado.

    Parameters
    ----------
    nombre : str
        Nombre del mercado.
    simbolo : str
        Símbolo de la acción.

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o si la acción está o no en el mercado.

    Raises
    ------
    Error
        Da error si no existe un mercado con el nombre que le pasamos.
    """
    if nombre not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre}"}
    mercado = Mercado._mercados_registrados[nombre]
    if simbolo in mercado:
        return {"mensaje": f"La acción cuyo símbolo es {simbolo} sí que está en el mercado {nombre}"}
    return {"mensaje": f"La acción cuyo símbolo es {simbolo} no que está en el mercado {nombre}"}


def igual_mercado(nombre1: str, nombre2: str) -> dict[str, str]:
    """
    Esta función sirve para ver si dos mercados son iguales en base a sus acciones.

    Parameters
    ----------
    nombre1 : str
        Nombre del primer mercado
    nombre2 : str
        Nombre del segundo mercado

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o si los mercados son iguales o no.

    Raises
    ------
    Error
        Da error si no existe alguno de los mercados que le pasamos.
    """
    if nombre1 not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre1}"}
    if nombre2 not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre2}"}
    mercado1 = Mercado._mercados_registrados[nombre1]
    mercado2 = Mercado._mercados_registrados[nombre2]
    if mercado1 == mercado2:
        return {"mensaje": f"Los mercados {nombre1} y {nombre2} son iguales"}
    else:
        return {"mensaje": f"Los mercados {nombre1} y {nombre2} no son iguales"}


def no_igual_mercado(nombre1: str, nombre2: str) -> dict[str, str]:
    """
    Esta función sirve para ver si dos mercados no son iguales en base a sus acciones.

    Parameters
    ----------
    nombre1 : str
        Nombre del primer mercado
    nombre2 : str
        Nombre del segundo mercado

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o si los mercados son iguales o no.

    Raises
    ------
    Error
        Da error si no existe alguno de los mercados que le pasamos.
    """
    if nombre1 not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre1}"}
    if nombre2 not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre2}"}
    mercado1 = Mercado._mercados_registrados[nombre1]
    mercado2 = Mercado._mercados_registrados[nombre2]
    if mercado1 != mercado2:
        return {"mensaje": f"Los mercados {nombre1} y {nombre2} no son iguales"}
    else:
        return {"mensaje": f"Los mercados {nombre1} y {nombre2} son iguales"}


def suma_mercados(nombre1: str, nombre2: str) -> dict[str, str]:
    """
    Esta función sirve para sumar dos mercados.

    Parameters
    ----------
    nombre1 : str
        Nombre del primer mercado
    nombre2 : str
        Nombre del segundo mercado

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o éxito.

    Raises
    ------
    Error
        Da error si no existe alguno de los mercados que le pasamos.
    Error
        Da error si el nombre combinado de ambos mercados ya pertenece a un mercado existente.
    """
    if nombre1 not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre1}"}
    if nombre2 not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre2}"}
    mercado1 = Mercado._mercados_registrados[nombre1]
    mercado2 = Mercado._mercados_registrados[nombre2]
    try:
        mercado = mercado1 + mercado2
        return {"mensaje": f"Los mercados {nombre1} y {nombre2} se han sumado correctamente creando {mercado.nombre}"}
    except:
        return {"error": f"Ya existe un mercado con el nombre combinado {nombre1 + '_' + nombre2}"}


def suma_propia(nombre1: str, nombre2: str) -> dict[str, str]:
    """
    Esta función sirve para sumar el segundo mercado al primero.

    Parameters
    ----------
    nombre1 : str
        Nombre del primer mercado
    nombre2 : str
        Nombre del segundo mercado

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o éxito.

    Raises
    ------
    Error
        Da error si no existe alguno de los mercados que le pasamos.
    """
    if nombre1 not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre1}"}
    if nombre2 not in Mercado._mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre2}"}
    mercado1 = Mercado._mercados_registrados[nombre1]
    mercado2 = Mercado._mercados_registrados[nombre2]
    mercado1 += mercado2
    return {"mensaje": "La suma se ha efectuado correctamente"}


# Clase Transaccion

def crear_transaccion(nombre: str, simbolo: str, cantidad: int) -> dict[str, str]:
    """
    Crea y ejecuta una transacción de compra para un inversor determinado.

    Parameters
    ----------
    nombre : str
        Nombre del inversor registrado
    simbolo : str
        Simbolo de la accion a comprar.
    cantindad : int
        Numero de acciones a adquirir.

    Returns
    -------
    dict[str, str]
        Un diccionario con un mensaje de éxito.

    Raises
    ------
    Error
        Si algo falla al realizar la operación.

    """
    if nombre not in inversores_registrados:
        return {"error": f"El inversor '{nombre}' no está registrado"}
    if simbolo not in Accion._acciones_registradas:
        return {"error": f"La acción con el símbolo {simbolo} no existe"}
    accion = Accion._acciones_registradas[simbolo]
    inversor = inversores_registrados[nombre]
    transaccion = Transaccion(inversor, accion, cantidad)

    if transaccion.validar_transaccion():
        transaccion.ejecutar_transaccion()
        inversor._transacciones.append(transaccion)
        exportar_transacciones_csv(inversor._transacciones)
        return {"mensaje": f"Transacción realizada: {transaccion}"}
    else:
        return {"error": "Fondos insuficientes para realizar la operación"}


def calcula_total_transacciones(nombre: str) -> dict[str, str]:
    """
    Calcula el total invertido por un inversor sumando todas sus transacciones.

    Parameters
    ----------
    nombre : str
        Nombre del inversor registrado.

    Returns
    -------
    dict[str, str]
        Un mensaje con el total invertido.

    Raises
    ------
    Error
        Si el nombre del inversor no está registrado.
    """
    if nombre not in inversores_registrados:
        return {"error": f"El inversor '{nombre}' no está registrado"}

    transacciones = inversores_registrados[nombre]._transacciones
    if not transacciones:
        return {"mensaje": "Este inversor no tiene transacciones registradas."}

    realizadas = 0
    for t in transacciones:
        realizadas += t.calcular_total()

    return {"mensaje": f"Total invertido por {nombre}: {round(realizadas, 2)}€"}


# Clase IA
def recomendacion(nombre: str) -> dict[str, str]:
    """
    Nos da una recomendación para un inversor en función de sus caracteristicas.

    Parameters
    ----------
    nombre : str
        Nombre del inversor.

    Returns
    -------
    dict[str,str]
        Nos devuelve un diccionario con una clave str (que será "error" o "mensaje") y un valor
        str que te dirá si ha habido un error o las recomendaciones deseadas.

    Raises
    ---------------
    Error
        Da error si no existe un inversor con el nombre que le pasamos.
    Error
        Da error si no hay suficiente capital para comprar ninguna acción.
    """
    if nombre not in inversores_registrados:
        return {"error": f"No hay ningún inversor cuyo nombre es {nombre}"}
    inversor = inversores_registrados[nombre]
    try:
        return {"mensaje": f"Las recomendaciones son {IA(inversor).recomendacion()}"}
    except:
        return {"error": "No tienes suficiente capital para comprar ninguna acción"}






