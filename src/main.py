import requests

BASE_URL = "http://127.0.0.1:8000" 


def listar_inversores():
    """
    Listado con todos los inversores almacenados en el sistema

    Realiza una solicitud Get al endpoint "/inversores" y devuelve el código
    de estado junto con la respuesta JSON
    """
    try:
        r = requests.get(f"{BASE_URL}/inversores")
        print(r.status_code, r.json())
    except requests.exceptions.ConnectionError:
        print("No se ha podido conectar con el servidor. ¿Está en ejecución?")
    except Exception as e:
        print(f"Error inesperado: {e}")

def crear_inversor():
    """
    Crea un nuevo inversor en el sistema y lo almacena

    Para ello necesitamos que el usuario introduzca el nombre, capital inicial y tipo
    de inversor, luego solicita con POST al endpoint "/inversores"

    Raises
    ------
    ValueError
        Si el capital introducido no es un número válido
    """
    nombre = input("Nombre del inversor: ")
    capital = input("Capital inicial: ")
    tipo = input("Tipo (IA | conservador | agresivo): ")

    try:
        capital_float = float(capital)
    except ValueError:
        print("Capital inválido. Debe ser un número.")
        return

    r = requests.post(
        f"{BASE_URL}/inversores",
        json={"nombre": nombre, "capital": capital_float, "tipo": tipo}
    )
    print(r.status_code, r.json())


def listar_acciones():
    """
    Devuelve un listado con todas las acciones disponibles

    Soloicita con GET al endpoint "/acciones" y muestra el código de estado y la respuesta JSON
    """
    r = requests.get(f"{BASE_URL}/acciones")
    print(r.status_code, r.json())


def crear_accion():
    """
    Crea una nueva accion y la almacena

    El usuario debe introducir el nombre y el precio inicial, luego hace una solicitud
    POST al endpoint "/acciones"

    Raises
    ------
    ValueError
        Si el precio ingresado no es un número válido
    """
    nombre = input("Nombre de la acción: ")
    precio = input("Precio inicial: ")

    try:
        precio_float = float(precio)
    except ValueError:
        print("Precio inválido. Debe ser un número.")
        return

    r = requests.post(
        f"{BASE_URL}/acciones",
        json={"nombre": nombre, "precio": precio_float}
    )
    print(r.status_code, r.json())

def listar_transacciones():
    """
    Lista todas las transacciones realizadas

    Hace una solicitud GET al endpoint "/transacciones" y muestra
    el código de estado y la respuesta JSON.
    """
    r = requests.get(f"{BASE_URL}/transacciones")
    print(r.status_code, r.json())


def crear_transaccion():
    """
    Crea una nueva transacción de compra/venta

    El usuario debe introducir el nombre del inversor, el nombre de la acción, tipo de
    operación y cantidad, luego realiza una solicitud POST al endpoint "/transacciones"

    Raises
    ------
    ValueError
        SI la cantidad de dinero ingresada no es un número válido
    """
    inversor = input("Nombre del inversor: ")
    accion = input("Nombre de la acción: ")
    tipo = input("Tipo (compra | venta): ")
    cantidad = input("Cantidad: ")

    try:
        cantidad_int = int(cantidad)
    except ValueError:
        print("Cantidad inválida. Debe ser un número entero.")
        return

    r = requests.post(
        f"{BASE_URL}/transacciones",
        json={
            "nombre_inversor": inversor,
            "nombre_accion": accion,
            "tipo": tipo,
            "cantidad": cantidad_int
        }
    )
    print(r.status_code, r.json())



def menu():
    """
    Muestra un menú interactivo para el cliente del simulador de bolsa

    Permite al usuario listar y crear inversores, acciones y transacciones,
    o salir del programa
    """
    while True:
        print("\n=== Simulador de Bolsa - Menú Cliente ===")
        print("1. Listar inversores")
        print("2. Crear inversor")
        print("3. Listar acciones")
        print("4. Crear acción")
        print("5. Listar transacciones")
        print("6. Crear transacción")
        print("7. Salir")

        opcion = input("Selecciona una opción (1-7): ")

        if opcion == '1':
            listar_inversores()
        elif opcion == '2':
            crear_inversor()
        elif opcion == '3':
            listar_acciones()
        elif opcion == '4':
            crear_accion()
        elif opcion == '5':
            listar_transacciones()
        elif opcion == '6':
            crear_transaccion()
        elif opcion == '7':
            print("Saliendo del cliente...")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()