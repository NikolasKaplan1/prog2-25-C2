import requests
from sys import exit

BASE_URL = "http://127.0.0.1:8000"
access_token = None

def listar_inversores():
    """
    Realiza una solicitud GET para obtener un listado de los inversores

    Raises
    ------
    requests.exceptions.ConnectionError:
        Si no se puede establecer conexión con el servidor
    Exception:
        Si hay otro error inesperado
    """
    try:
        r = requests.get(f"{BASE_URL}/inversores")
        print(r.status_code, r.json())
    except requests.exceptions.ConnectionError:
        print("No se ha podido conectar con el servidor. ¿Está en ejecución?")
    except Exception as e:
        print(f"Error inesperado: {e}")


def buscar_inversor():
    """
    Solicita el ID del inversor para realiza una solicitud GET y mostrar la 
    informaión de dicho inversor

    Raises
    ------
    ValueError:
        Si el ID proporcionado no es correcto
    Exception:
        Si hay algún error en la solicitud HTTP
    """
    inversor_id = input("ID del inversor: ")
    try:
        id_int = int(inversor_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    try:
        r = requests.get(f"{BASE_URL}/inversores/{id_int}")
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def crear_inversor():
    """
    Solicita los datos para poder crear un nuevo inversor, los valida y sube al servidor
    utilizando POST

    Raises
    ------
    ValueError:
        Si el capital ingresado no es un número
    Exception:
        Si hay algún error en la solicitud HTTP
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

    try:
        r = requests.post(
            f"{BASE_URL}/inversores",
            json={
                "nombre": nombre,
                "apellidos": apellidos,
                "email": email,
                "contrasena": contrasena,
                "tarjeta_credito": tarjeta_credito,
                "capital": capital_float
            }
        )
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def modificar_inversor():
    """
    Modifica los datos de un inversor existente, omitiendo los campos en los que no
    se introducen datos para modificar

    Raises
    ------
    ValueError:
        Si el ID o el nuevo capital no son válidos
    Exception:
        Si hay algún error en la solicitud HTTP
    """
    inversor_id = input("ID del inversor a modificar: ")

    try:
        id_int = int(inversor_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    print("Deja vacío cualquier campo que no quieras modificar")
    nombre = input("Nuevo nombre: ")
    apellidos = input("Nuevos apellidos: ")
    email = input("Nuevo email: ")
    contrasena = input("Nueva contraseña: ")
    tarjeta_credito = input("Nueva tarjeta de crédito: ")
    capital = input("Nuevo capital: ")

    data = {}
    if nombre:
        data["nombre"] = nombre
    if apellidos:
        data["apellidos"] = apellidos
    if email:
        data["email"] = email
    if contrasena:
        data["contrasena"] = contrasena
    if tarjeta_credito:
        data["tarjeta_credito"] = tarjeta_credito
    if capital:
        try:
            data["capital"] = float(capital)
        except ValueError:
            print("El capital debe ser un número")
            return

    try:
        r = requests.put(f"{BASE_URL}/inversores/{id_int}", json=data)
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def eliminar_inversor():
    """
    Elimina un inversor dado su ID

    Raises
    ------
    ValueError:
        Si el ID no es un entero
    Exception:
        Si hay algún error en la solicitud HTTP
    """
    inversor_id = input("ID del inversor: ")
    try:
        id_int = int(inversor_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    try:
        r = requests.delete(f"{BASE_URL}/inversores/{id_int}")
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def listar_acciones():
    """
    Realiza una solicitud GET para obtener un listado de las acciones

    Raises
    ------
    Exception:
        Si hay un error inesperado
    """
    try:
        r = requests.get(f"{BASE_URL}/acciones")
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def buscar_accion():
    """
    Solicita el ID de la acción para realiza una solicitud GET y mostrar la 
    informaión de dicho acción

    Raises
    ------
    ValueError:
        Si el ID proporcionado no es correcto
    Exception:
        Si hay algún error en la solicitud HTTP
    """
    accion_id = input("ID de la acción: ")
    try:
        id_int = int(accion_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    try:
        r = requests.get(f"{BASE_URL}/acciones/{id_int}")
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def crear_accion():
    """
    Solicita los datos para poder crear una nueva acción, los valida y sube al servidor
    utilizando POST

    Raises
    ------
    ValueError:
        Si el precio ingresado no es un número
    Exception:
        Si hay algún error en la solicitud HTTP
    """
    nombre = input("Nombre de la acción: ")
    simbolo = input("Símbolo: ")
    precio = input("Precio inicial: ")
    sector = input("Sector: ")

    try:
        precio_float = float(precio)
    except ValueError:
        print("El precio debe ser un número")
        return

    try:
        r = requests.post(
            f"{BASE_URL}/acciones",
            json={
                "nombre": nombre,
                "simbolo": simbolo,
                "precio_actual": precio_float,
                "sector": sector
            }
        )
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def modificar_accion():
    """
    Modifica los datos de una acción existente, omitiendo los campos en los que no
    se introducen datos para modificar

    Raises
    ------
    ValueError:
        Si el ID o el nuevo precio no son válidos
    Exception:
        Si hay algún error en la solicitud HTTP
    """
    accion_id = input("ID de la acción: ")

    print("Deja vacío cualquier campo que no quieras modificar")
    nombre = input("Nombre: ")
    simbolo = input("Símbolo: ")
    precio_actual = input("Precio actual: ")
    sector = input("Sector: ")

    data = {}
    if nombre:
        data["nombre"] = nombre
    if simbolo:
        data["simbolo"] = simbolo
    if precio_actual:
        try:
            data["precio_actual"] = float(precio_actual)
        except ValueError:
            print("El precio debe ser un número")
            return
    if sector:
        data["sector"] = sector

    try:
        r = requests.put(f"{BASE_URL}/acciones/{accion_id}", json=data)
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def eliminar_accion():
    """
    Elimina una acción dado su ID

    Raises
    ------
    ValueError:
        Si el ID no es un entero
    Exception:
        Si hay algún error en la solicitud HTTP
    """
    accion_id = input("ID de la acción: ")
    try:
        id_int = int(accion_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    try:
        r = requests.delete(f"{BASE_URL}/acciones/{id_int}")
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def listar_transacciones():
    """
    Realiza una solicitud GET para obtener un listado de las transacciones

    Raises
    ------
    Exception:
        Si hay un error inesperado
    """
    try:
        r = requests.get(f"{BASE_URL}/transacciones")
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def buscar_transaccion():
    """
    Solicita el ID de la transacción para realiza una solicitud GET y mostrar la 
    informaión de la transacción

    Raises
    ------
    ValueError:
        Si el ID proporcionado no es correcto
    Exception:
        Si hay algún error en la solicitud HTTP
    """
    transaccion_id = input("ID de la transacción: ")
    try:
        id_int = int(transaccion_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    try:
        r = requests.get(f"{BASE_URL}/transacciones/{id_int}")
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def buscar_transaccion_inversor():
    """
    Solicita el ID del inversor para realiza una solicitud GET y mostrar la 
    informaión de la transacción relacionada con el inversor

    Raises
    ------
    ValueError:
        Si el ID proporcionado no es correcto
    Exception:
        Si hay algún error en la solicitud HTTP
    """
    inversor_id = input("ID del inversor: ")
    try:
        id_int = int(inversor_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    try:
        r = requests.get(f"{BASE_URL}/transacciones/inversor/{id_int}")
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def buscar_transaccion_accion():
    """
    Solicita el ID de la acción para realiza una solicitud GET y mostrar la 
    informaión de la transacción relacionada con la acción

    Raises
    ------
    ValueError:
        Si el ID proporcionado no es correcto
    Exception:
        Si hay algún error en la solicitud HTTP
    """
    accion_id = input("ID de la acción: ")
    try:
        id_int = int(accion_id)
    except ValueError:
        print("ID inválido, debe ser un número entero")
        return

    try:
        r = requests.get(f"{BASE_URL}/transacciones/accion/{id_int}")
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def crear_transaccion():
    """
    Solicita los datos para poder crear una nueva transacción, los valida y sube al servidor
    utilizando POST

    Raises
    ------
    ValueError:
        Si la cantidad o precio ingresados no son valores numéricos
    Exception:
        Si hay algún error en la solicitud HTTP
    """
    inversor_id = input("ID del inversor: ")
    accion_id = input("ID de la acción: ")
    tipo = input("Tipo (compra | venta): ")
    cantidad = input("Cantidad: ")
    precio = input("Precio: ")
    fecha = input("Fecha (YYYY-MM-DD): ")

    try:
        cantidad_int = int(cantidad)
        precio_float = float(precio)
    except ValueError:
        print("Cantidad y precio deben ser números")
        return

    try:
        r = requests.post(
            f"{BASE_URL}/transacciones",
            json={
                "inversor_id": int(inversor_id),
                "accion_id": int(accion_id),
                "tipo": tipo,
                "cantidad": cantidad_int,
                "precio": precio_float,
                "fecha": fecha
            }
        )
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def eliminar_transaccion():
    """
    Elimina una transacción dado su ID

    Raises
    ------
    ValueError:
        Si el ID no es un entero
    Exception:
        Si hay algún error en la solicitud HTTP
    """
    transaccion_id = input("ID de la transacción: ")
    try:
        id_int = int(transaccion_id)
    except ValueError:
        print("ID debe ser un número entero")
        return

    try:
        r = requests.delete(f"{BASE_URL}/transacciones/{id_int}")
        print(r.status_code, r.json())
    except Exception as e:
        print(f"Error: {e}")


def autenticacion():
    """
    Gestiona el proceso de registro e inicio de sesión del usuario, necesario para
    acceder al menú principal del cliente

    Returns
    -------
    bool:
        True si la autenticación fue exitosa, False en caso contrario.
    """
    global access_token

    while True:
        print("\n***** INICIO DE SESIÓN *****")
        print("1. Registro")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Selecciona una opción (1-3): ")

        if opcion == '1':
            nombre = input("Nombre: ")
            apellidos = input("Apellidos: ")
            email = input("Email: ")
            contrasena = input("Contraseña: ")
            tarjeta_credito = input("Tarjeta de crédito: ")
            capital = input("Capital inicial: ")

            try:
                capital_float = float(capital)
            except ValueError:
                print("El capital debe ser un número")
                continue

            try:
                r = requests.post(
                    f"{BASE_URL}/autenticaciones/register",
                    json={
                        "nombre": nombre,
                        "apellidos": apellidos,
                        "email": email,
                        "contrasena": contrasena,
                        "tarjeta_credito": tarjeta_credito,
                        "capital": capital_float
                    }
                )
                print(r.status_code, r.json())
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == '2':
            email = input("Email: ")
            contrasena = input("Contraseña: ")
            try:
                r = requests.post(
                    f"{BASE_URL}/autenticaciones/login",
                    json={"email": email, "contrasena": contrasena}
                )
                if r.status_code == 200:
                    access_token = r.json().get("access_token")
                    print("Sesión iniciada correctamente")
                    return True
                else:
                    print(f"Error: {r.status_code} - {r.json().get('detail')}")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == '3':
            print("Saliendo...")
            exit()
        else:
            print("Opción no válida")

def menu():
    """
    Muestra un menú con todas las acciones que puede realizar un cliente
    """
    while True:
        print("\n***** MENÚ CLIENTE *****")
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

        op = input("Selecciona una opción (1-17): ")

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
    if autenticacion():
        menu()
