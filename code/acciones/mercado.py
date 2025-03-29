class Mercado:
    def __init__(self, lista_acciones: list[Accion]):
        self.lista_acciones = lista_acciones
    def registrar_accion(self, accion: Accion):
        self.lista_acciones.append(accion)
    def obtener_precio(self,simbolo: str) -> float:
        for accion in self.lista_acciones:
            if accion.simbolo == simbolo:
                return accion.precio_actual
    def simular_movimientos
        pass