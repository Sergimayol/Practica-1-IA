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
        pass


class Estado:
    def __init__(self, info: dict, coste: int, padre=None):
        self.__info = info  # información sobre la rana
        self.__padre = padre  # padre del estado
        self.__coste = coste  # coste del estado
        self.__max_tablero = 7

    def __hash__(self) -> int:
        return hash(tuple(self.__info))

    @property
    def info(self):
        return self.__info

    def es_meta(self) -> bool:
        # TODO: comprobar si la rana esta en la meta
        # la implementación actual es para hacer pruebas
        return (
            self.__info.get(ClauPercepcio.POSICIO).get("Miquel")
            == self[ClauPercepcio.OLOR]
        )

    def calcula_heuristica(self):
        """Método que calcula la heurística del estado pasado por parámetro.

        Args:
            estado (Estado): Estado del que se quiere calcular la heurística.

        Returns:
            int: Valor de la heurística.
        """
        
        resultado = 0
        resultado += abs(self.__info.get(ClauPercepcio.POSICIO).get("Miquel") - self.__info.get(ClauPercepcio.OLOR))
        #Habría que sumar el peso también
        return resultado


    def padre(self):
        return self.__padre

    def __str__(self) -> str:
        return str(self.__info)

    def get_frog_names(self) -> list[str]:
        return list(self.__info.get(ClauPercepcio.POSICIO).keys())

    def legal(self, pos_actual: tuple) -> bool:
        # obtener los muros
        walls = self.__info.get(ClauPercepcio.PARETS)
        # comprobar si la posicion actual esta en los muros
        return pos_actual not in walls

    def generar_hijos(self, nombre_rana: str) -> list:
        """
        Esta funcion genera los posibles estados hijos de un estado,
        siempre y cuando sean legales.

        Args:
            nombre_rana (_str_): nombre de la rana que se desea generar los hijos

        Returns:
            _list_: list de estados hijos generados
        """
        debug, print_hijos = False, False

        hijos = []

        # pos 0 = x, pos 1 = y (empiezan en 0)
        pos_actual = self.__info.get(ClauPercepcio.POSICIO).get(nombre_rana)

        if pos_actual[0] > 0:
            # movimientos a la izquierda
            new_pos = (pos_actual[0] - 1, pos_actual[1])
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(Estado(hijo, self.__coste + 1, self))

            if debug:
                print("movimiento a la izquierda +1")
                print("hijo: ", hijo)

            if pos_actual[0] > 1:
                new_pos = (pos_actual[0] - 2, pos_actual[1])
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(Estado(hijo, self.__coste + 2, self))

                if debug:
                    print("movimiento a la izquierda +2")
                    print("hijo: ", hijo)

        if pos_actual[0] < self.__max_tablero:
            # movimientos a la derecha
            new_pos = (pos_actual[0] + 1, pos_actual[1])
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(Estado(hijo, self.__coste + 1, self))

            if debug:
                print("movimiento a la derecha +1")
                print("hijo: ", hijo)

            if pos_actual[0] < self.__max_tablero - 1:
                new_pos = (pos_actual[0] + 2, pos_actual[1])
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(Estado(hijo, self.__coste + 2, self))

                if debug:
                    print("movimiento a la derecha +2")
                    print("hijo: ", hijo)

        if pos_actual[1] > 0:
            # movimientos hacia arriba
            new_pos = (pos_actual[0], pos_actual[1] - 1)
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(Estado(hijo, self.__coste + 1, self))

            if debug:
                print("movimiento hacia arriba +1")
                print("hijo: ", hijo)

            if pos_actual[1] > 1:
                new_pos = (pos_actual[0], pos_actual[1] - 2)
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(Estado(hijo, self.__coste + 2, self))

                if debug:
                    print("movimiento hacia arriba +2")
                    print("hijo: ", hijo)

        if pos_actual[1] < self.__max_tablero:
            # movimientos hacia abajo
            new_pos = (pos_actual[0], pos_actual[1] + 1)
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(Estado(hijo, self.__coste + 1, self))

            if debug:
                print("movimiento hacia abajo +1")
                print("hijo: ", hijo)

            if pos_actual[1] < self.__max_tablero - 1:
                new_pos = (pos_actual[0], pos_actual[1] + 2)
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(Estado(hijo, self.__coste + 2, self))

                if debug:
                    print("movimiento hacia abajo +2")
                    print("hijo: ", hijo)

        return hijos
