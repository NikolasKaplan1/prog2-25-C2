import controlador as control

def crear_accion():
    simbolo = obtener_input("Ingrese símbolo de la acción: ")
    nombre = obtener_input("Ingrese nombre de la acción: ")
    resultado = dame_estudiantes_curso(id_curso, año)

    print(resultado.get("error") or resultado.get("mensaje"))
   