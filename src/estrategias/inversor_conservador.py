from models.inversor import Inversor

class InversorConservador(Inversor): # prefiere seguridad y estabilidad
    def recomendar_compra(self):
        """
        Recomienda las dos acciones más baratas de la cartera.

        Returns
        -------------
        list[str]
            Lista con nombre y precio de las acciones recomendadas.
        """
        acciones = list(self.cartera.values())  # lista de [Accion, cantidad]

        lista_precios = []
        for accion, _ in acciones:
            lista_precios.append([accion, accion.precio_actual])

        for i in range(len(lista_precios)):
            for j in range(i + 1, len(lista_precios)):
                if lista_precios[i][1] > lista_precios[j][1]:
                    lista_precios[i], lista_precios[j] = lista_precios[j], lista_precios[i]

        recomendaciones = []
        for i in range(min(2, len(lista_precios))):
            accion = lista_precios[i][0]
            recomendaciones.append(accion.nombre + " a " + str(round(accion.precio_actual, 2)) + "€")

        return recomendaciones