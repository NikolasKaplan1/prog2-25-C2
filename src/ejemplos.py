import controlador as control

def crear_accion():
    simbolo = input("Ingrese símbolo de la acción: ")
    nombre = input("Ingrese nombre de la acción: ")
    precio_actual = float(input("Ingrese el precio actual de la acción: "))
    historial_input = input("Ingrese el historial de precios en formato fecha:precio separados por comas (ej: 2024-01-01:100,2024-01-02:102.5): ")
    
    historial_precios = {}
    try:
        for entrada in historial_input.split(","):
            fecha, precio = entrada.split(":")
            historial_precios[fecha.strip()] = float(precio.strip())
    except ValueError:
        print("Error en el formato del historial. Asegúrate de escribirlo como fecha:precio, separados por comas.")
        return
    resultado = control.crear_accion(simbolo, nombre, precio_actual, historial_precios)
    print(resultado.get("error") or resultado.get("mensaje"))

def crear_accion_real():
    simbolo = input("Ingrese símbolo de la acción real: ")
    resultado = control.crear_accion_real(simbolo)
    print(resultado.get("error") or resultado.get("mensaje"))

def actualizar_precio():
    simbolo = input("Ingrese el símbolo de la acción: ")
    nuevo_precio = float(input("Ingrese el precio nuevo de la acción: "))
    resultado = control.actualizar_precio(simbolo,nuevo_precio)
    print(resultado.get("error") or resultado.get("mensaje"))

def actualizar_precio_real():
    simbolo = input("Ingrese el símbolo de la acción real: ")
    resultado = control.actualizar_precio_real(simbolo)
    print(resultado.get("error") or resultado.get("mensaje"))

def datos_accion():
    simbolo = input("Ingrese el símbolo de la acción: ")
    resultado = control.datos_accion(simbolo)
    print(resultado.get("error") or resultado.get("mensaje"))

def crea_inversor():
    nombre = input("Ingrese el nombre del inversor: ")
    capital = float(input("Ingrese el capital del inversor: "))
    tipo = input("Ingrese el tipo de inversor que es: ")
    resultado = control.crea_inversor(nombre, capital, tipo)
    print(resultado.get("error") or resultado.get("mensaje"))

def datos_inversor(nombre: str):
    nombre = input("Ingrese el nombre del inversor: ")
    resultado = control.datos_inversor(nombre)
    if "error" in resultado:
        print(resultado.get("error"))
    else:
        print(f"Capital: {resultado[capital]}, tipo: {resultado[tipo]}")

def mostrar_cartera():
    nombre = input("Ingrese el nombre del inversor: ")
    resultado = control.mostrar_cartera(nombre)
    print(resultado.get("error") or resultado.get("mensaje"))


def comprar_accion():
    nombre = input("Ingrese el nombre del inversor: ")
    simbolo = input("Ingrese el simbolo de la acción que quiere comprar: ")
    cantidad = int(input("Ingrese la cantidad de acciones que quiere comprar: "))
    resultado = control.comprar_accion(nombre, simbolo, cantidad)
    print(resultado.get("error") or resultado.get("mensaje"))

    
def vender_accion():
    nombre = input("Ingrese el nombre del inversor: ")
    simbolo = input("Ingrese el simbolo de la acción que quiere vender: ")
    cantidad = int(input("Ingrese la cantidad de acciones que quiere vender: "))
    resultado = control.vender_accion(nombre, simbolo, cantidad)
    print(resultado.get("error") or resultado.get("mensaje"))

def mostrar_transaccion_registrada():
    nombre = input("Ingrese el nombre del inversor: ")
    resultado = control.mostrar_transaccion_registrada(nombre)
    print(resultado.get("error") or resultado.get("mensaje"))


def comprar_acciones_con_operador():
    nombre = input("Ingrese el nombre del inversor: ")
    simbolo = input("Ingrese el simbolo de la acción que quiere comprar: ")
    cantidad = int(input("Ingrese la cantidad de acciones que quiere comprar: "))
    resultado = control.comprar_accion_con_operador(nombre, simbolo, cantidad)
    print(resultado.get("error") or resultado.get("mensaje"))


def vender_acciones_con_operador():
    nombre = input("Ingrese el nombre del inversor: ")
    simbolo = input("Ingrese el simbolo de la acción que quiere comprar: ")
    cantidad = int(input("Ingrese la cantidad de acciones que quiere comprar: "))
    resultado = control.vender_accion_con_operador(nombre, simbolo, cantidad)
    print(resultado.get("error") or resultado.get("mensaje"))

def crear_mercado():
    nombre = input("Ingrese el nombre del mercado: ")
    lista_acciones = input("Ingrese las acciones con sus símbolos (simbolo1, simbolo2, ...): ").split(", ")
    resultado = control.crear_mercado(nombre, lista_acciones)
    print(resultado.get("error") or resultado.get("mensaje"))

def registrar_accion():
    nombre = input("Ingrese el nombre del mercado: ")
    simbolo = input("Ingrese el símbolo de la acción a registrar: ")
    resultado = control.registrar_accion(nombre, simbolo)
    print(resultado.get("error") or resultado.get("mensaje"))

def obtener_precio():
    nombre = input("Ingrese el nombre del mercado: ")
    simbolo = input("Ingrese el símbolo de la acción de la que quiere obtener el precio: ")
    resultado = control.obtener_precio(nombre, simbolo)
    print(resultado.get("error") or resultado.get("precio"))

def bancarrota():
    nombre = input("Ingrese el nombre del mercado: ")
    simbolo = input("Ingrese el símbolo de la acción a declarar en bancarrota: ")
    resultado = control.bancarrota(nombre, simbolo)
    print(resultado.get("error") or resultado.get("mensaje"))

def simular_movimientos():
    nombre = input("Ingrese el nombre del mercado: ")
    resultado = control.simular_movimientos(nombre)
    print(resultado.get("error") or resultado.get("mensaje"))

def crear_transaccion():
    nombre = input("Ingrese el nombre del inversor: ")
    simbolo = input("Ingrese el símbolo de la acción: ")
    cantidad = int(input("Ingrese la cantidad de acciones de la transacción: "))
    resultado = control.crear_transaccion(nombre, simbolo, cantidad)
    print(resultado.get("error") or resultado.get("mensaje"))

def calcula_total_transacciones():
    nombre = input("Ingrese el nombre del inversor: ")
    resultado = control.calcula_total_transacciones(nombre)
    print(resultado.get("error") or resultado.get("mensaje"))

def recomendacion():
    nombre = input("Ingrese el nombre del inversor al que quiere recomendar: ")
    resultado = control.recomendacion(nombre)
    print(resultado.get("error") or resultado.get("mensaje"))

    def menu():
    opciones = {
        '1': crear_accion,
        '2': crear_accion_real,
        '3': actualizar_precio,
        '4': actualizar_precio_real,
        '5': datos_accion,
        '6': crea_inversor,
        '7': datos_inversor,
        '8': mostrar_cartera,
        '9': comprar_accion,
        '10': vender_accion,
        '11': mostrar_transaccion_registrada,
        '12': comprar_acciones_con_operador,
        '13': vender_acciones_con_operador,
        '14': crear_mercado,
        '15': registrar_accion,
        '16': obtener_precio,
        '17': bancarrota,
        '18': simular_movimiento,
        '19': crear_transaccion,
        '20': calcula_total_transacciones,
        '21': recomendacion,
        '0': guardar_y_salir
    }

    while True:
        print("\nMenú del sistema:")
        print("1. Crear una acción")
        print("2. Crear una acción con datos reales")
        print("3. Actualizar el precio de una acción")
        print("4. Actualizar el precio de una acción con datos reales")
        print("5. Ver los datos de una acción")
        print("6. Crear un inversor")
        print("7. Obtener los datos de un inversor")
        print("8. Mostrar la cartera de un inversor")
        print("9. Comprar una acción")
        print("10. Vender una acción")
        print("11. Mostrar transacciones registradas de un inversor")
        print("12. Comprar acciones con el operador")
        print("13. Vender acciones con el operador")
        print("14. Crear un mercado")
        print("15. Registrar una acción en un mercado")
        print("16. Obtener el precio de una acción en un mercado")
        print("17. Declarar en bancarrota una acción que está en un mercado")
        print("18. Simular un movimiento de bolsa en un mercado")
        print("19. Crear una transacción")
        print("20. Calcular el total de transacciones que ha hecho un inversor")
        print("21. Recomienda unas acciones para un inversor")
        print("0. Guardar y salir")

        opcion = nput("Seleccione una opción: ")

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
   