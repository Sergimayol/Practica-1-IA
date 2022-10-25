"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc, entorn as entorn_practica1
import copy
from practica1.entorn import ClauPercepcio



class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)

    def pinta(self, display):
        pass

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        # Implmentar aquí lógica agente
        # Estado inicial de la rana
        estado_inicial = Estado(percep[entorn_practica1.ClauPercepcio.POSICIO], 0, padre=None)
        estado_inicial.generar_hijos()
        # EN un futuro cambiar, de momento es para que no de error
        return entorn_practica1.AccionsRana.ESPERAR

class Estado:
    def __init__(self, info: str, coste: int, padre=None):
        self.__info = info   #[posicio, olor, parets]
        self.__padre = padre # Estado
        self.__coste = coste # Coste de las acciones

    def __hash__(self) -> int:
        return hash(tuple(self.__info))

    @property
    def info(self):
        return self.__info

    def es_meta(self) -> bool:
        return self.__info == entorn_practica1.ClauPercepcio.OLOR

    def padre(self):
        return self.__padre
    
    def __str__(self) -> str:
        return str(self.__info)

    def legal(self) -> bool:
        # Comprobar si el movimiento es legal
        if [ClauPercepcio.PARETS] == entorn_practica1.Direccio.ESQUERRE:
            return False
        
        if [ClauPercepcio.PARETS] == entorn_practica1.Direccio.DRETA:
            return False

        if [ClauPercepcio.PARETS] == entorn_practica1.Direccio.DALT:
            return False
        
        if [ClauPercepcio.PARETS] == entorn_practica1.Direccio.BAIX:
            return False
        return True
    
    # Método para generar hijos de un estado
    def generar_hijos(self):
        hijos = [] # Lista de estados
        for columna in range(len(self.__info)):
            for fila in range(len(self.__info)):
                if not self.es_meta():
                    estadoAux = copy.deepcopy(self.__info)
                    hijos.append(estadoAux)

                    print(estadoAux)

        #print(hijos)
        return hijos

        # Primero para generar los hijos debemos saber el estado inicial y el estado final
        # sabiendo el estado inicial de la pizza y el estado inicial de la rana, podemos calcular de la forma que nos convenga
        # es decir, si por ejemplo tenemos la pizza en la posición (0,0) y la rana en la posición (1,1) entonces sabemos que la rana debe igualar la posición de la pizza
        # y hará los movimientos basados en el algoritmo de búsqueda hasta llegar a la posición.

