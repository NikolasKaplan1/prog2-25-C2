
from typing import List

from inversor import Inversor
from acciones import Accion

class InversorConservador(Inversor):
    """
    Inversor consdrvador que hereda de la clase Inversor

    Métodos
    ------------
    recomendar_compra
    
    """
    def recomendar_compra(self) -> List[Accion]:
        pass



class InversorAgresivo(Inversor):
    """
    Inversor agresicvo que hereda de la clase Inversor

    Métodos
    -----------
    recomendar_compra    
    """
    def recomendar_compra(self) -> List[Accion]:
        pass