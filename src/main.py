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


def buscar_inversor():
    inversor_id = input("ID del inversor: ")
    try:
        id_int = int(inversor_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    r = requests.get(f"{BASE_URL}/inversores", json={"id": id_int})
    print(r.status_code, r.json())

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
    apellidos = input("Apellidos del inversor: ")
    email = input("Email del inversor: ")
    contrasena = input("Contraseña del inversor: ")
    tarjeta_credito = input("Tarjeta de crédito: ")
    capital = input("Capital inicial: ")

    try:
        capital_float = float(capital)
    except ValueError:
        print("Capital inválido. Debe ser un número.")
        return

    r = requests.post(
        f"{BASE_URL}/inversores",
        json={"nombre": nombre, "apellidos": apellidos, "email": email, "contrasena": contrasena, "tarjeta_credito": tarjeta_credito, "capital": capital_float}
    )
    print(r.status_code, r.json())


def modificar_inversor():
    pass

def eliminar_inversor():
    inversor_id = input("ID del inversor: ")
    try:
        id_int = int(inversor_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    r = requests.delete(f"{BASE_URL}/inversores", json={"id": id_int})
    print(r.status_code, r.json())


def listar_acciones():
    """
    Devuelve un listado con todas las acciones disponibles

    Soloicita con GET al endpoint "/acciones" y muestra el código de estado y la respuesta JSON
    """
    r = requests.get(f"{BASE_URL}/acciones")
    print(r.status_code, r.json())

def buscar_accion():
    accion_id = input("ID de la accion: ")
    try:
        id_int = int(accion_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    r = requests.get(f"{BASE_URL}/acciones", json={"id": id_int})
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
    simbolo = input("Símbolo: ")
    precio = input("Precio inicial: ")
    sector = input("Sector: ")

    try:
        precio_float = float(precio)
    except ValueError:
        print("Precio inválido. Debe ser un número.")
        return

    r = requests.post(
        f"{BASE_URL}/acciones",
        json={"nombre": nombre, "simbolo": simbolo, "precio_actual": precio_float, "sector": sector}
    )
    print(r.status_code, r.json())

def modificar_accion():
    accion_id = input("ID de la acción: ")


def eliminar_accion():
    accion_id = input("ID de la acción: ")

    try:
        id_int = int(accion_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    r = requests.delete(f"{BASE_URL}/acciones", json={"id": id_int})
    print(r.status_code, r.json())

def listar_transacciones():
    """
    Lista todas las transacciones realizadas

    Hace una solicitud GET al endpoint "/transacciones" y muestra
    el código de estado y la respuesta JSON.
    """
    r = requests.get(f"{BASE_URL}/transacciones")
    print(r.status_code, r.json())


def buscar_transaccion():
    transaccion_id = input("ID de la transaccion: ")
    try:
        id_int = int(transaccion_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    r = requests.get(f"{BASE_URL}/transacciones", json={"id": id_int})
    print(r.status_code, r.json())    

def buscar_transaccion_inversor():
    inversor_id = input("ID del inversor: ")
    try:
        id_int = int(inversor_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    r = requests.get(f"{BASE_URL}/inversor", json={"id": id_int})
    print(r.status_code, r.json())    

def buscar_transaccion_accion():
    accion_id = input("ID del accion: ")
    try:
        id_int = int(accion_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    r = requests.get(f"{BASE_URL}/accion", json={"id": id_int})
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
    inversor_id = input("ID del inversor: ")
    accion_id = input("ID de la acción: ")
    tipo = input("Tipo (compra | venta): ")
    cantidad = input("Cantidad: ")
    precio = input("Precio: ")
    fecha = input("Fecha: ")

    try:
        cantidad_int = int(cantidad)
    except ValueError:
        print("Cantidad inválida. Debe ser un número entero.")
        return

    r = requests.post(
        f"{BASE_URL}/transacciones",
        json={
            "inversor_id": inversor_id,
            "accion_id": accion_id,
            "tipo": tipo,
            "cantidad": cantidad_int,
            "precio": precio,
            "fecha": fecha
        }
    )
    print(r.status_code, r.json())

def eliminar_transaccion():
    transaccion_id = input("ID de la transacción: ")

    try:
        id_int = int(transaccion_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    r = requests.delete(f"{BASE_URL}/transacciones", json={"id": id_int})
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
        print("2. Buscar inversor")
        print("3. Crear inversor")
        print("4. Modificar inversor")
        print("5. Eliminar inversor")
        print("6. Listar acciones")
        print("7. Buscar acción")
        print("8. Crear acción")
        print("9. Modificar acción")
        print("10. Eliminar acción")
        print("11. Listar transacciones")
        print("12. Buscar transacción")
        print("13. Buscar transacción por inversor")
        print("14. Buscar transacción por acción")
        print("15. Crear transacción")
        print("16. Eliminar transacción")
        print("17. Salir")

        op = input("Selecciona una opción (1-7): ")

        if op == '1':
            listar_inversores()
        elif op == '2':
            buscar_inversor()
        elif op == '3':
            crear_inversor()
        elif op == '4':
            modificar_inversor()
        elif op == '5':
            eliminar_inversor()
        elif op == '6':
            listar_acciones()
        elif op == '7':
            buscar_accion()
        elif op == '8':
            crear_accion()
        elif op == '9':
            modificar_accion()
        elif op == '10':
            eliminar_accion()
        elif op == '11':
            listar_transacciones()
        elif op == '12':
            buscar_transaccion()
        elif op == '13':
            buscar_transaccion_inversor()
        elif op == '14':
            buscar_transaccion_accion()
        elif op == '15':
            crear_transaccion()
        elif op == '16':
            eliminar_transaccion()
        elif op == '17':
            print("Saliendo del cliente...")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()