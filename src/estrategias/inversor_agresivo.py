from models.inversor import Inversor

class InversorAgresivo(Inversor): 
    """
    Inversor con estrategia agresiva.
    Prefiere invertir en acciones de precio alto, buscando ganancias rápidas 
    aunque implique mayor riesgo.

    Hereda de:
    ----------
    Inversor

    Methods
    -------
    recomendar_compra()
        Recomienda las acciones más caras de la cartera a comprar.
    """

    def recomendar_compra(self) -> list[str]:
        """
        Recomienda las acciones más caras de la cartera.

        Returns
        -------
        list[str]
            lista con los nombres y precios de las acciones más caras recomendadas.
       
        """
        acciones = list(self._Inversor__cartera.values())
        lista_precios = []
        for accion, _ in acciones:
            lista_precios.append([accion, accion.precio_actual])

        for i in range(len(lista_precios)):
            for j in range(i + 1, len(lista_precios)):
                if lista_precios[i][1] < lista_precios[j][1]: # ordena de mayor a menor (estrategia agresiva)
                    lista_precios[i], lista_precios[j] = lista_precios[j], lista_precios[i]

        recomendaciones = []
        for i in range(min(2, len(lista_precios))):
            accion = lista_precios[i][0]
            recomendaciones.append(accion.nombre + " a " + str(round(accion.precio_actual, 2)) + "€")

        return recomendaciones