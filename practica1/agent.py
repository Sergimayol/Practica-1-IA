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
        estado_inicial = Estado(percep[ClauPercepcio.POSICIO], 0, padre=None)
        # EN un futuro cambiar, de momento es para que no de error
        return entorn_practica1.AccionsRana.ESPERAR


class Estado:
    def __init__(self, info: dict, coste: int, padre=None):
        self.__info = info  # [posicio, olor, parets]
        self.__padre = padre  # Estado
        self.__coste = coste  # Coste de las acciones
        self.__max_tablero = 7

    def __hash__(self) -> int:
        return hash(tuple(self.__info))

    @property
    def info(self):
        return self.__info

    def es_meta(self) -> bool:
        return (
            self.__info.get(ClauPercepcio.POSICIO).get("Miquel")
            == self[ClauPercepcio.OLOR]
        )

    def padre(self):
        return self.__padre

    def __str__(self) -> str:
        return str(self.__info)

    def legal(self, pos_actual: tuple) -> bool:
        # obtener los muros
        walls = self.__info.get(ClauPercepcio.PARETS)
        # comprobar si la posicion actual esta en los muros
        if pos_actual in walls:
            return False
        return True

    def estado_inicial(self):
        hijo = copy.deepcopy(self.__info)
        print("hijo: ", hijo)
        print("info: ", self.__info)
        print("claves: ", self.__info.keys())
        # Get all the keys
        keys = list(self.__info.keys())
        print("keys: ", keys)

        return 0

    # Método para generar hijos de un estado
    def generar_hijos(self, nombre_rana):
        debug = False

        if debug:
            self.estado_inicial()

        hijos = []  # Lista de estados

        pos_actual = self.__info.get(ClauPercepcio.POSICIO).get(nombre_rana)
        # print("pos_actual: ", pos_actual)

        # print("info: ", self.__info)
        # pos 0 = x, pos 1 = y (empiezan en 0)
        if pos_actual[0] > 0:
            # movimientos a la izquierda
            hijo = copy.deepcopy(self.__info)
            new_pos = (pos_actual[0] - 1, pos_actual[1])
            if self.legal(new_pos):
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(Estado(hijo, self.__coste + 1, self))

            if debug:
                print("movimiento a la izquierda +1")
                print("hijo: ", hijo)

            if pos_actual[0] > 1:
                hijo = copy.deepcopy(self.__info)
                new_pos = (pos_actual[0] - 2, pos_actual[1])
                if self.legal(new_pos):
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(Estado(hijo, self.__coste + 2, self))

                if debug:
                    print("movimiento a la izquierda +2")
                    print("hijo: ", hijo)

        if pos_actual[0] < self.__max_tablero:
            # movimientos a la derecha
            hijo = copy.deepcopy(self.__info)
            new_pos = (pos_actual[0] + 1, pos_actual[1])
            if self.legal(new_pos):
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(Estado(hijo, self.__coste + 1, self))

            if debug:
                print("movimiento a la derecha +1")
                print("hijo: ", hijo)

            if pos_actual[0] < self.__max_tablero - 1:
                hijo = copy.deepcopy(self.__info)
                new_pos = (pos_actual[0] + 2, pos_actual[1])
                if self.legal(new_pos):
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(Estado(hijo, self.__coste + 2, self))

                if debug:
                    print("movimiento a la derecha +2")
                    print("hijo: ", hijo)

        if pos_actual[1] > 0:
            # movimientos hacia arriba
            hijo = copy.deepcopy(self.__info)
            new_pos = (pos_actual[0], pos_actual[1] - 1)
            if self.legal(new_pos):
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(Estado(hijo, self.__coste + 1, self))

            if debug:
                print("movimiento hacia arriba +1")
                print("hijo: ", hijo)

            if pos_actual[1] > 1:
                hijo = copy.deepcopy(self.__info)
                new_pos = (pos_actual[0], pos_actual[1] - 2)
                if self.legal(new_pos):
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(Estado(hijo, self.__coste + 2, self))

                if debug:
                    print("movimiento hacia arriba +2")
                    print("hijo: ", hijo)

        if pos_actual[1] < self.__max_tablero:
            # movimientos hacia abajo
            hijo = copy.deepcopy(self.__info)
            new_pos = (pos_actual[0], pos_actual[1] + 1)
            if self.legal(new_pos):
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(Estado(hijo, self.__coste + 1, self))

            if debug:
                print("movimiento hacia abajo +1")
                print("hijo: ", hijo)

            if pos_actual[1] < self.__max_tablero - 1:
                hijo = copy.deepcopy(self.__info)
                new_pos = (pos_actual[0], pos_actual[1] + 2)
                if self.legal(new_pos):
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(Estado(hijo, self.__coste + 2, self))

                if debug:
                    print("movimiento hacia abajo +2")
                    print("hijo: ", hijo)

        # for hijo in hijos:
        #   print("hijo: ", hijo.info.get(ClauPercepcio.POSICIO))

        return hijos

        # Primero para generar los hijos debemos saber el estado inicial y el estado final
        # sabiendo el estado inicial de la pizza y el estado inicial de la rana, podemos calcular de la forma que nos convenga
        # es decir, si por ejemplo tenemos la pizza en la posición (0,0) y la rana en la posición (1,1) entonces sabemos que la rana debe igualar la posición de la pizza
        # y hará los movimientos basados en el algoritmo de búsqueda hasta llegar a la posición generando los hijos pertinentes.
