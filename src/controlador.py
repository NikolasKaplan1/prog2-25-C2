from models.__init__ import Accion, AccionReal, Inversor, Mercado, Transaccion
from estrategias.inversor_agresivo import InversorAgresivo
from estrategias.inversor_conservador import InversorPasivo
from typing import Union
import random
import yfinance as yf

#Clases Accion y AccionReal
def crear_accion(simbolo: str, nombre: str, precio_actual: float, historial_precios: dict[str,float]):
    if simbolo in Accion.acciones_registradas:
        return {"error": f"Ya existe una acción con el símbolo {simbolo}"}
    Accion(simbolo, nombre, precio_actual, historial_precios)
    return {"mensaje": "Acción añadida correctamente"}


def crear_accion_real(simbolo: str):
    repr = yf.Ticker(simbolo) #esto da una representación de la acción real con su símbolo
    data = repr.history(period="365d") #nos da los datos del último año
    if data.empty:
        return {"error": f"No se encontraron datos para la acción con el símbolo {simbolo} en este último año"}
    if simbolo in Accion.acciones_registradas:
        return {"error": f"Ya existe una acción con el símbolo {simbolo}"}
    AccionReal(simbolo)
    return {"mensaje": "Acción añadida correctamente"}

def actualizar_precio(simbolo: str,nuevo_precio: float):
    if simbolo not in Accion.acciones_registradas:
        return {"error": f"No existe una acción con el símbolo {simbolo}"}
    Accion.acciones_registradas[simbolo].actualizar_precio(nuevo_precio)
    return {"mensaje": "Precio actualizado correctamente"}

def actualizar_precio_real(simbolo: str):
    if simbolo not in Accion.acciones_registradas:
        return {"error": f"No existe una acción con el símbolo {simbolo}"}
    accion = Accion.acciones_registradas[simbolo]
    if type(accion) is not AccionReal:
        return {"error": f"La acción con el símbolo {simbolo} no es una acción real"}
    accion.actualizar_precio()
    return {"mensaje": "Precio actualizado correctamente"}

def datos_accion(simbolo:str):
    if simbolo not in Accion.acciones_registradas:
        return {"error": f"No existe una acción con el símbolo {simbolo}"}
    accion = Accion.acciones_registradas[simbolo]
    return str(accion)

#Clase Inversor

inversores_registrados = {}
def crea_inversor(nombre: str, capital: float, tipo: str):
    """
    Crea un inversor nuevo y lo guarda en el diccionario de inversores.

    Tipo: puede ser de tipo agresivo o conservador(pasivo)
    """
    if nombre in inversores_registrados:
        return {"Error": f"Ya existe un inversor bajo el nombre: {nombre}"}
    if tipo == "Agresivo":
        inversores_registrados[nombre] = InversorAgresivo(nombre, capital)
    elif tipo == "Pasivo":
        inversores_registrados[nombre] = InversorPasivo(nombre, capital)
    else:
        return "Error: Tipo de inversor no válido."
    return f"Inversor {nombre} creado exitosamente como {tipo}"


def listar_inversores(nombre: str):
    """
    Devuelve la lista de todos los inversores registrados con su capital y tipo.

    """
    if nombre not in inversores_registrados:
        return {"Error": f"El inversor '{nombre}' no está registrado"}
    
    inversor = inversores_registrados[nombre]
    if isinstance(inversor, InversorAgresivo):
        tipo = "Agresivo"
    else:
        tipo = "Pasivo"
    return {
        nombre: {
            "Capital": round(inversor.capital, 2), 
            "tipo": tipo
        }
    }

def mostrar_cartera(nombre: str):
    if nombre not in inversores_registrados:
        return {"Error": f"El inversor '{nombre}' no está registrado"}
    inversor = inversores_registrados[nombre]
    return inversor.mostrar_cartera()


def comprar_accion(nombre: str, accion: Accion, cantidad: int):
    """
    Permite a un inversor comprar una cantidad determinada de acciones.

    Parametros
    -----------
    - nombre(str) : nombre del inversor
    - accion(Accion) : Objeto de la clase accion
    - cantidad(int) : numero de acciones a comprar
    """
    if nombre not in inversores_registrados:
        return {"Error": f"El inversor '{nombre}' no está registrado"}
    inversor = inversores_registrados[nombre]
    try:
        inversor.comprar(accion, cantidad)
        return f"{nombre} ha comprado {cantidad} acciones de {accion.nombre} exitosamente"
    except ValueError as e:
        return {"error": str(e)}
    
def vender_accion(nombre: str, accion: Accion, cantidad: int):
    """
    Permite a un inversor vender una cantidad determinada de acciones.

    Parametros
    -----------
    - nombre(str) : nombre del inversor
    - accion(Accion) : Objeto de la clase accion
    - cantidad(int) : numero de acciones a comprar
    """
    if nombre not in inversores_registrados:
        return {"Error": f"El inversor '{nombre}' no está registrado"}
    inversor = inversores_registrados[nombre]
    try:
        inversor.vender(accion, cantidad)
        return f"{nombre} ha vendido {cantidad} acciones de {accion.nombre} exitosamente"
    except ValueError as e:
        return {"error": str(e)}

def mostrar_transaccion_registrada(nombre: str):
    if nombre not in inversores_registrados:
        return {"Error": f"El inversor '{nombre}' no está registrado"}
    inversor = inversores_registrados[nombre]
    if not inversor.transacciones:
        return "Este inversor no ha realizado ninguna transacción."
    resumen_transacciones = f"Historial de transacciones de {nombre}:\n"
    for transaccion in inversor.transacciones:
        resumen_transacciones += str(transaccion) + "\n"
    return resumen_transacciones

# Utiliza la sobrecarga del operador + para comprar acciones
def comprar_acciones_con_operador(nombre: str, accion: Accion, cantidad: int):
    if nombre not in inversores_registrados:
        return {"Error": f"El inversor '{nombre}' no está registrado"}
    
    inversor = inversores_registrados[nombre]
    try:
        inversor + (accion, cantidad)
        return f"{nombre} ha comprado {cantidad} acciones de {accion.nombre} usando el operador '+'."
    except Exception as e:
        return {"error": str(e)}


def vender_acciones_con_operador(nombre: str, accion: Accion, cantidad: int):
    if nombre not in inversores_registrados:
        return {"Error": f"El inversor '{nombre}' no está registrado"}
    
    inversor = inversores_registrados[nombre]
    try:
        inversor - (accion, cantidad)
        return f"{nombre} ha vendido {cantidad} acciones de {accion.nombre} usando el operador '-'."
    except Exception as e:
        return {"error": str(e)}






#Clase Mercado
def crear_mercado(nombre: str, lista_acciones: list[Accion]):
    if nombre in mercados_registrados:
        return {"error": f"Ya existe un mercado con el nombre {nombre}"}
    
    for i in range(len(lista_acciones)):
        accion = lista_acciones[i]
        if accion in lista_acciones[:i]:
            return {"error": f"No puede haber acciones repetidas"}
        if not isinstance(accion,Accion):
            return {"error": f"El objeto {accion}, que es el término {i}, no pertenece a la clase Accion"}
    Mercado(nombre,lista_acciones)
    return {"mensaje": "Mercado creado correctamente"}
    
def registrar_accion(nombre, accion: Accion):
    if not isinstance(accion,Accion):
        return {"error": f"El objeto {accion} no pertenece a la clase Accion"}
    
    if nombre not in Mercado.mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre}"}
    
    if accion in Mercado.mercados_registrados[nombre].lista_acciones:
        return {"error": f"La acción {accion} ya está en el mercado {nombre}"}
    Mercado.mercados_registrados[nombre].registrar_accion(accion)
        
def obtener_precio(nombre,simbolo: str) -> Union[float,str]:
    if nombre not in Mercado.mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre}"}
    mercado = Mercado.mercados_registrados[nombre]
    

def bancarrota(self,simbolo: str):
    if nombre not in Mercado.mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre}"}
    mercado = Mercado.mercados_registrados[nombre]
    for accion in mercado.lista_acciones:
        if accion.simbolo == simbolo:
            mercado.bancarrota(simbolo)
            return {"error": f"La empresa con símbolo {simbolo} se ha declarado en bancarrota exitosamente"}
    return {"error": f"No se encontró la acción con símbolo {simbolo} en el mercado {nombre}"}
        
def simular_movimientos(self):
    if nombre not in Mercado.mercados_registrados:
        return {"error": f"No existe un mercado con el nombre {nombre}"}
    
    for accion in self.lista_acciones:
        variacion = random.uniform(-0.3, 0.3)
        nuevo_precio = round(accion.precio_actual * (1 + variacion), 3)
        accion.actualizar_precio(nuevo_precio)


      



