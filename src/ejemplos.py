import controlador as control


def crear_accion() -> None:
    """
    Esta función crea una nueva acción.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Raises
    ------
    ValueError
        Nos dará error si el formato del historial es incorrecto.
    """
    simbolo = input("Ingrese símbolo de la acción: ")
    nombre = input("Ingrese nombre de la acción: ")
    precio_actual = float(input("Ingrese el precio actual de la acción: "))
    historial_input = input(
        "Ingrese el historial de precios en formato fecha:precio separados por comas (ej: 2024-01-01:100,2024-01-02:102.5): ")

    historial_precios = {}
    try:
        for entrada in historial_input.split(","):
            fecha, precio = entrada.split(":")
            historial_precios[fecha.strip()] = float(precio.strip())
    except ValueError:
        print("Error en el formato del historial. Asegúrate de escribirlo como fecha:precio, separados por comas.")
    resultado = control.crear_accion(simbolo, nombre, precio_actual, historial_precios)
    print(resultado.get("error") or resultado.get("mensaje"))


def crear_accion_real() -> None:
    """
    Esta función crea una nueva acción real.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    simbolo = input("Ingrese símbolo de la acción real: ")
    resultado = control.crear_accion_real(simbolo)
    print(resultado.get("error") or resultado.get("mensaje"))


def actualizar_precio() -> None:
    """
    Esta función actualiza el precio de una acción.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    simbolo = input("Ingrese el símbolo de la acción: ")
    nuevo_precio = float(input("Ingrese el precio nuevo de la acción: "))
    resultado = control.actualizar_precio(simbolo, nuevo_precio)
    print(resultado.get("error") or resultado.get("mensaje"))


def actualizar_precio_real() -> None:
    """
    Esta función actualiza el precio de una acción con sus valores reales.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    simbolo = input("Ingrese el símbolo de la acción real: ")
    resultado = control.actualizar_precio_real(simbolo)
    print(resultado.get("error") or resultado.get("mensaje"))


def datos_accion() -> None:
    """
    Esta función nos muestra los datos de una acción.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    simbolo = input("Ingrese el símbolo de la acción: ")
    resultado = control.datos_accion(simbolo)
    print(resultado.get("error") or resultado.get("mensaje"))


def menor_que() -> None:
    """
    Esta función sirve para comparar si una acción es menor a otra en base a su precio.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    simbolo1 = input("Ingrese el símbolo de la primera acción: ")
    simbolo2 = input("Ingrese el símbolo de la segunda acción: ")
    resultado = control.menor_que(simbolo1, simbolo2)
    print(resultado.get("error") or resultado.get("mensaje"))


def mayor_que() -> None:
    """
    Esta función sirve para comparar si una acción es mayor a otra en base a su precio.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    simbolo1 = input("Ingrese el símbolo de la primera acción: ")
    simbolo2 = input("Ingrese el símbolo de la segunda acción: ")
    resultado = control.mayor_que(simbolo1, simbolo2)
    print(resultado.get("error") or resultado.get("mensaje"))


def crea_inversor() -> None:
    """
    Esta función crea un inversor.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del inversor: ")
    capital = float(input("Ingrese el capital del inversor: "))
    tipo = input("Ingrese el tipo de inversor que es: ")
    resultado = control.crea_inversor(nombre, capital, tipo)
    print(resultado.get("error") or resultado.get("mensaje"))


def datos_inversor() -> None:
    """
    Esta función devuelve los datos de un inversor.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del inversor: ")
    resultado = control.datos_inversor(nombre)
    if "error" in resultado:
        print(resultado.get("error"))
    else:
        print(f"Nombre: {resultado["nombre"]}, capital: {resultado["capital"]}, tipo: {resultado["tipo"]}")


def mostrar_cartera() -> None:
    """
    Esta función muestra la cartera de un inversor.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del inversor: ")
    resultado = control.mostrar_cartera(nombre)
    print(resultado.get("error") or resultado.get("mensaje"))


def comprar_accion() -> None:
    """
    Esta función sirve para que un inversor compre una acción.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del inversor: ")
    simbolo = input("Ingrese el simbolo de la acción que quiere comprar: ")
    cantidad = int(input("Ingrese la cantidad de acciones que quiere comprar: "))
    resultado = control.comprar_accion(nombre, simbolo, cantidad)
    print(resultado.get("error") or resultado.get("mensaje"))


def vender_accion() -> None:
    """
    Esta función sirve para que un inversor venda una acción.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del inversor: ")
    simbolo = input("Ingrese el simbolo de la acción que quiere vender: ")
    cantidad = int(input("Ingrese la cantidad de acciones que quiere vender: "))
    resultado = control.vender_accion(nombre, simbolo, cantidad)
    print(resultado.get("error") or resultado.get("mensaje"))


def mostrar_transaccion_registrada() -> None:
    """
    Esta función sirve para mostrar una transaccion registrada.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del inversor: ")
    resultado = control.mostrar_transaccion_registrada(nombre)
    print(resultado.get("error") or resultado.get("mensaje"))


def comprar_acciones_con_operador() -> None:
    """
    Esta función sirve para que un inversor compre acciones con el operador.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del inversor: ")
    simbolo = input("Ingrese el simbolo de la acción que quiere comprar: ")
    cantidad = int(input("Ingrese la cantidad de acciones que quiere comprar: "))
    resultado = control.comprar_accion_con_operador(nombre, simbolo, cantidad)
    print(resultado.get("error") or resultado.get("mensaje"))


def vender_acciones_con_operador() -> None:
    """
    Esta función sirve para que un inversor venda acciones con el operador.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del inversor: ")
    simbolo = input("Ingrese el simbolo de la acción que quiere comprar: ")
    cantidad = int(input("Ingrese la cantidad de acciones que quiere comprar: "))
    resultado = control.vender_accion_con_operador(nombre, simbolo, cantidad)
    print(resultado.get("error") or resultado.get("mensaje"))


def crear_mercado() -> None:
    """
    Esta función sirve para crear un mercado financiero.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del mercado: ")
    lista_acciones = input("Ingrese las acciones con sus símbolos (simbolo1, simbolo2, ...): ").split(", ")
    resultado = control.crear_mercado(nombre, lista_acciones)
    print(resultado.get("error") or resultado.get("mensaje"))


def datos_mercado() -> None:
    """
    Esta función sirve para imprimir los datos del mercado con el nombre que le pasamos.
    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del mercado: ")
    resultado = control.datos_mercado(nombre)
    print(resultado.get("error") or resultado.get("mensaje"))


def registrar_accion() -> None:
    """
    Esta función sirve para registrar una acción en un mercado.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del mercado: ")
    simbolo = input("Ingrese el símbolo de la acción a registrar: ")
    resultado = control.registrar_accion(nombre, simbolo)
    print(resultado.get("error") or resultado.get("mensaje"))


def obtener_precio() -> None:
    """
    Esta función sirve para obtener el precio de una acción que está en un mercado.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del mercado: ")
    simbolo = input("Ingrese el símbolo de la acción de la que quiere obtener el precio: ")
    resultado = control.obtener_precio(nombre, simbolo)
    print(resultado.get("error") or resultado.get("precio"))

def eliminar_accion() -> None:
    """
    Esta función sirve para eliminar una acción de un mercado.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del mercado: ")
    simbolo = input("Ingrese el símbolo de la acción que quiere eliminar: ")
    resultado = control.eliminar_accion(nombre, simbolo)
    print(resultado.get("error") or resultado.get("precio"))
def bancarrota() -> None:
    """
    Esta función sirve para declarar en bancarrota una acción de un mercado.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del mercado: ")
    simbolo = input("Ingrese el símbolo de la acción a declarar en bancarrota: ")
    resultado = control.bancarrota(nombre, simbolo)
    print(resultado.get("error") or resultado.get("mensaje"))


def simular_movimientos() -> None:
    """
    Esta función sirve para simular movimientos en un mercado.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del mercado: ")
    resultado = control.simular_movimientos(nombre)
    print(resultado.get("error") or resultado.get("mensaje"))


def tamaño() -> None:
    """
    Esta función devuelve el tamaño de un mercado en base al número de acciones que contiene.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del mercado: ")
    resultado = control.tamaño(nombre)
    print(resultado.get("error") or resultado.get("mensaje"))


def obtener_accion() -> None:
    """
    Esta función sirve para obtener la acción de un mercado dado un item.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del mercado: ")
    item = int(input("Ingrese el índice de la acción: "))
    resultado = control.obtener_accion(nombre, item)
    print(resultado.get("error") or resultado.get("mensaje"))


def contener() -> None:
    """
    Esta función sirve para ver si una acción está contenida en un mercado.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del mercado: ")
    simbolo = input("Ingrese el símbolo de la acción: ")
    resultado = control.contener(nombre, simbolo)
    print(resultado.get("error") or resultado.get("mensaje"))


def igual_mercado() -> None:
    """
    Esta función sirve para ver si dos mercados son iguales en base a sus acciones.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre1 = input("Ingrese el nombre del primer mercado: ")
    nombre2 = input("Ingrese el nombre del segundo mercado: ")
    resultado = control.igual_mercado(nombre1, nombre2)
    print(resultado.get("error") or resultado.get("mensaje"))


def no_igual_mercado() -> None:
    """
    Esta función sirve para ver si dos mercados no son iguales en base a sus acciones.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre1 = input("Ingrese el nombre del primer mercado: ")
    nombre2 = input("Ingrese el nombre del segundo mercado: ")
    resultado = control.no_igual_mercado(nombre1, nombre2)
    print(resultado.get("error") or resultado.get("mensaje"))


def suma_mercados() -> None:
    """
    Esta función sirve para sumar dos mercados.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre1 = input("Ingrese el nombre del primer mercado: ")
    nombre2 = input("Ingrese el nombre del segundo mercado: ")
    resultado = control.suma_mercados(nombre1, nombre2)
    print(resultado.get("error") or resultado.get("mensaje"))


def suma_propia() -> None:
    """
    Esta función sirve para sumar el segundo mercado al primero.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre1 = input("Ingrese el nombre del primer mercado: ")
    nombre2 = input("Ingrese el nombre del segundo mercado: ")
    resultado = control.suma_propia(nombre1, nombre2)
    print(resultado.get("error") or resultado.get("mensaje"))


def crear_transaccion() -> None:
    """
    Esta función sirve para crear una transacción.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del inversor: ")
    simbolo = input("Ingrese el símbolo de la acción: ")
    cantidad = int(input("Ingrese la cantidad de acciones de la transacción: "))
    resultado = control.crear_transaccion(nombre, simbolo, cantidad)
    print(resultado.get("error") or resultado.get("mensaje"))


def calcula_total_transacciones() -> None:
    """
    Esta función sirve para calcular el total de una transacción.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del inversor: ")
    resultado = control.calcula_total_transacciones(nombre)
    print(resultado.get("error") or resultado.get("mensaje"))


def recomendacion() -> None:
    """
    Esta función sirve para obtener recomendación de compra de acciones.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del inversor al que quiere recomendar: ")
    resultado = control.recomendacion(nombre)
    print(resultado.get("error") or resultado.get("mensaje"))


def contiene_accion_inversor() -> None:
    """
    Esta función verifica si un inversor tiene una acción específica en su cartera.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Nombre del inversor: ")
    simbolo = input("Simbolo de la accion: ")
    resultado = control.contiene_accion(nombre, simbolo)
    print(resultado.get("error") or resultado.get("mensaje"))


def comparar_inversores() -> None:
    """
    Esta función compara si dos inversores han invertido en las mismas empresas.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre1 = input("Nombre del inversor: ")
    nombre2 = input("Nombre del inversor: ")
    resultado = control.comparar_inversores(nombre1, nombre2)
    print(resultado.get("error") or resultado.get("mensaje"))


def obtener_informacion_transaccion() -> None:
    """
    Esta función permite consultar un dato específico de una transacción realizada por un inversor.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del inversor: ")
    num_transaccion = int(input("Ingrese el número de transacción (posición en la lista): "))
    campo = input("Ingrese dato a consultar (inversor, accion,simbolo, cantidad, precio, fecha): ")
    resultado = control.datos_transaccion(nombre, index, campo)
    print(resultado.get("error") or resultado.get("mensaje"))


def contiene_accion_inversor() -> None:
    """
    Esta función verifica si un inversor tiene una acción específica en su cartera.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Nombre del inversor: ")
    simbolo = input("Simbolo de la accion: ")
    resultado = control.inversor_contiene_accion(nombre, simbolo)
    print(resultado.get("error") or resultado.get("mensaje"))


def comparar_inversores() -> None:
    """
    Esta función compara si dos inversores han invertido en las mismas empresas.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre1 = input("Nombre del inversor: ")
    nombre2 = input("Nombre del inversor: ")
    resultado = control.comparar_inversores(nombre1, nombre2)
    print(resultado.get("error") or resultado.get("mensaje"))


def obtener_informacion_transaccion() -> None:
    """
    Esta función permite consultar un dato específico de una transacción realizada por un inversor.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    nombre = input("Ingrese el nombre del inversor: ")
    num_transaccion = int(input("Ingrese el número de transacción (posición en la lista): "))
    campo = input("Ingrese dato a consultar (inversor, accion,simbolo, cantidad, precio, fecha): ")
    resultado = control.datos_transaccion(nombre, index, campo)
    print(resultado.get("error") or resultado.get("mensaje"))


def guardar_y_salir() -> None:
    print("Saliendo del sistema...")


def menu() -> None:
    """
    Esta función es el menú del programa.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    opciones = {
        '1': crear_accion,
        '2': crear_accion_real,
        '3': actualizar_precio,
        '4': actualizar_precio_real,
        '5': datos_accion,
        '6': menor_que,
        '7': mayor_que,
        '8': crea_inversor,
        '9': datos_inversor,
        '10': mostrar_cartera,
        '11': comprar_accion,
        '12': vender_accion,
        '13': mostrar_transaccion_registrada,
        '14': comprar_acciones_con_operador,
        '15': vender_acciones_con_operador,
        '16': crear_mercado,
        '17': datos_mercado,
        '18': registrar_accion,
        '19': obtener_precio,
        '20': eliminar_accion,
        '21': bancarrota,
        '22': simular_movimientos,
        '23': tamaño,
        '24': obtener_accion,
        '25': contener,
        '26': igual_mercado,
        '27': no_igual_mercado,
        '28': suma_mercados,
        '29': suma_propia,
        '30': crear_transaccion,
        '31': calcula_total_transacciones,
        '32': recomendacion,
        '33': contiene_accion_inversor,
        '34': comparar_inversores,
        '35': obtener_informacion_transaccion,
        '0': guardar_y_salir
    }

    while True:
        print("\nMenú del sistema:")
        print("1. Crear una acción")
        print("2. Crear una acción con datos reales")
        print("3. Actualizar el precio de una acción")
        print("4. Actualizar el precio de una acción con datos reales")
        print("5. Ver los datos de una acción")
        print("6. Ver si el precio de una acción es menor que la de otra")
        print("7. Ver si el precio de una acción es mayor que la de otra")
        print("8. Crear un inversor")
        print("9. Obtener los datos de un inversor")
        print("10. Mostrar la cartera de un inversor")
        print("11. Comprar una acción")
        print("12. Vender una acción")
        print("13. Mostrar transacciones registradas de un inversor")
        print("14. Comprar acciones con el operador")
        print("15. Vender acciones con el operador")
        print("16. Crear un mercado")
        print("17. Ver los datos de un mercado")
        print("18. Registrar una acción en un mercado")
        print("19. Obtener el precio de una acción en un mercado")
        print("20. Eliminar una acción de un mercado")
        print("21. Declarar en bancarrota una acción que está en un mercado")
        print("22. Simular un movimiento de bolsa en un mercado")
        print("23. Ver el tamaño de un mercado (la cantidad de acciones que tiene)")
        print("24. Ver una acción que está en una posición determinada del mercado")
        print("25. Comprobar si una acción está en un mercado")
        print("26. Comprobar si dos mercados son iguales en base a sus acciones")
        print("27. Comprobar si dos mercados no son iguales en base a sus acciones")
        print("28. Sumar dos mercados")
        print("29. Sumar al primer mercado el segundo mercado")
        print("30. Crear una transacción")
        print("31. Calcular el total de transacciones que ha hecho un inversor")
        print("32. Recomienda unas acciones para un inversor")
        print("33. Verificar si un inversor tiene una acción (operador 'in')")
        print("34. Comparar si dos inversores tienen las mismas empresas en su cartera")
        print("35. Consultar un campo específico de una transacción")
        print("0. Guardar y salir")

        opcion = input("Seleccione una opción: ")

        if opcion in opciones:
            opciones[opcion]()

            if opcion == '0':
                break
            else:
                input("Presione Enter para continuar...")
        else:
            print("Opción no válida. Intente de nuevo.")


# -----------------------------
# Función principal
# -----------------------------

if __name__ == "__main__":
    menu()


