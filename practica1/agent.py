"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc, entorn as entorn_practica1
import copy
from practica1.entorn import ClauPercepcio, AccionsRana, Direccio



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
    def __init__(self, info: dict, coste: int, padre=None):
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
        hijo = copy.deepcopy(self.__info) #Pasamos la información inicial del estado
        pos_inicial = hijo.get('Miquel') #Se devuelve la tupla inicial
        hijos.append(pos_inicial) #Se añade la tupla inicial a la lista de hijos
        # Se generan los hijos
        # Movimientos posibles
        # Se comprueba si es legal

        #pos_inicial[0] = Columna
        #pos_inicial[1] = Fila
        # Se mueve a la derecha
        if (pos_inicial[0] + 1, pos_inicial[1]) not in hijos:
            #Si no está en la última columna
            if (pos_inicial[0]<7):
                #Añadimos el hijo
                actual = (pos_inicial[0] + 1, pos_inicial[1])
                hijos.append(Estado(actual, self.__coste + 1, (self, (AccionsRana.MOURE, Direccio.DRETA))))
        # Se mueve a la izquierda
        if (pos_inicial[0] - 1, pos_inicial[1]) not in hijos:
            #Si no está en la primera columna
            if (pos_inicial[0]>0):
                #Añadimos el hijo
                actual = (pos_inicial[0] - 1, pos_inicial[1])
                hijos.append(Estado(actual, self.__coste + 1, (self, (AccionsRana.MOURE, Direccio.ESQUERRE))))
        # Se mueve hacia arriba
        if (pos_inicial[0], pos_inicial[1] + 1) not in hijos:
            #Si no está en la primera fila
            if (pos_inicial[1]>0):
                #Añadimos el hijo
                actual = (pos_inicial[0], pos_inicial[1] + 1)
                hijos.append(Estado(actual, self.__coste + 1, (self, (AccionsRana.MOURE, Direccio.DALT))))
        # Se mueve hacia abajo
        if (pos_inicial[0], pos_inicial[1] - 1) not in hijos:
            #Si no está en la ultima fila
            if (pos_inicial[1] < 7):
                #Añadimos el hijo
                actual = (pos_inicial[0], pos_inicial[1] - 1)
                hijos.append(Estado(actual, self.__coste + 1, (self, (AccionsRana.MOURE, Direccio.BAIX))))

        #print(hijos)
        #Devolvemos los hijos
        return hijos

        # Primero para generar los hijos debemos saber el estado inicial y el estado final
        # sabiendo el estado inicial de la pizza y el estado inicial de la rana, podemos calcular de la forma que nos convenga
        # es decir, si por ejemplo tenemos la pizza en la posición (0,0) y la rana en la posición (1,1) entonces sabemos que la rana debe igualar la posición de la pizza
        # y hará los movimientos basados en el algoritmo de búsqueda hasta llegar a la posición generando los hijos pertinentes.

