from queue import PriorityQueue
import sys
import time
from agent import Rana
from ia_2022 import entorn
from practica1.entorn import AccionsRana, ClauPercepcio, Direccio
import copy


class Estado:
    COSTE_MOVERSE = 1
    COSTE_ESPERAR = 0.5
    COSTE_SALTAR = 6

    def __init__(
        self,
        info: dict,
        coste: int,
        padre=None,
        direccion: Direccio = None,
        accion: AccionsRana = None,
    ):
        self.__info = info  # información sobre la rana
        self.__padre = padre  # padre del estado
        self.__coste = coste  # coste del estado
        self.__direccion = direccion  # direccion del estado
        self.__accion = accion  # accion del estado
        self.__max_tablero = 7

    def __hash__(self) -> int:
        return hash(tuple(self.__info))

    def get_direccion(self) -> Direccio or None:
        return self.__direccion

    def get_accion(self) -> AccionsRana or None:
        return self.__accion

    @property
    def info(self):
        return self.__info

    def es_meta(self, nombre_rana: str) -> bool:
        return self.__info.get(ClauPercepcio.POSICIO).get(
            nombre_rana
        ) == self.__info.get(ClauPercepcio.OLOR)

    @property
    def padre(self):
        return self.__padre

    @padre.setter
    def padre(self, value):
        self.__padre = value

    def __getitem__(self, key):
        if key == 0:
            return self.__info.get(ClauPercepcio.POSICIO)
        elif key == 1:
            return self.__info.get(ClauPercepcio.OLOR)
        elif key == 2:
            return self.__info.get(ClauPercepcio.PARETS)

    def __setitem__(self, key, value):
        self.__info[key] = value

    def __str__(self) -> str:
        return f"Estado: {self.__info}, Coste: {self.__coste}, Padre: {self.__padre}, Direccion: {self.__direccion}, Accion: {self.__accion}"

    def __eq__(self, __o: object) -> bool:
        return self.__info.get(ClauPercepcio.POSICIO) == __o.info.get(
            ClauPercepcio.POSICIO
        )

    def __lt__(self, __o: object) -> bool:
        return False

    def calcular_heuritica(self, nombre_rana: str) -> int:
        """Calcula la heuristica del estado. La heuristica
        es la distancia de la rana a la comida más el coste
        del estado.

        Args:
            nombre_rana (str): nombre de la rana

        Returns:
            int: heuristica del estado
        """
        # obtener la posicion de la rana
        pos_rana = self.__info.get(ClauPercepcio.POSICIO).get(nombre_rana)
        # obtener la posicion del olor
        pos_olor = self.__info.get(ClauPercepcio.OLOR)
        # calcular la distancia de Manhattan y añadir el coste
        return (
            abs(pos_rana[0] - pos_olor[0])
            + abs(pos_rana[1] - pos_olor[1])
            + self.__coste
        )

    def get_frog_names(self) -> list[str]:
        return list(self.__info.get(ClauPercepcio.POSICIO).keys())

    def legal(self, pos_actual: tuple) -> bool:
        """Comprueba si la posición actual no esta dentro de las paredes

        Args:
            pos_actual (tuple): posición actual

        Returns:
            bool: True si la posición actual no esta dentro de las paredes, False en caso contrario
        """
        walls = self.__info.get(ClauPercepcio.PARETS)
        return pos_actual not in walls

    def generar_hijos(self, nombre_rana: str) -> list:
        """Esta funcion genera los posibles estados hijos de un estado,
        siempre y cuando sean legales.

        Args:
            nombre_rana (str): nombre de la rana que se desea generar los hijos

        Returns:
            hijos (list): lista de estados hijos generados
        """
        hijos = []
        # pos 0 = x, pos 1 = y (empiezan en 0)
        pos_actual = self.__info.get(ClauPercepcio.POSICIO).get(nombre_rana)

        if pos_actual[0] > 0:
            # movimientos a la izquierda
            new_pos = (pos_actual[0] - 1, pos_actual[1])
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(
                    Estado(
                        hijo,
                        self.__coste + self.COSTE_MOVERSE,
                        self,
                        Direccio.ESQUERRE,
                        AccionsRana.MOURE,
                    )
                )

            if pos_actual[0] > 1:
                new_pos = (pos_actual[0] - 2, pos_actual[1])
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(
                        Estado(
                            hijo,
                            self.__coste + self.COSTE_SALTAR,
                            self,
                            Direccio.ESQUERRE,
                            AccionsRana.BOTAR,
                        )
                    )

        if pos_actual[0] < self.__max_tablero:
            # movimientos a la derecha
            new_pos = (pos_actual[0] + 1, pos_actual[1])
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(
                    Estado(
                        hijo,
                        self.__coste + self.COSTE_MOVERSE,
                        self,
                        Direccio.DRETA,
                        AccionsRana.MOURE,
                    )
                )

            if pos_actual[0] < self.__max_tablero - 1:
                new_pos = (pos_actual[0] + 2, pos_actual[1])
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(
                        Estado(
                            hijo,
                            self.__coste + self.COSTE_SALTAR,
                            self,
                            Direccio.DRETA,
                            AccionsRana.BOTAR,
                        )
                    )

        if pos_actual[1] > 0:
            # movimientos hacia arriba
            new_pos = (pos_actual[0], pos_actual[1] - 1)
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(
                    Estado(
                        hijo,
                        self.__coste + self.COSTE_MOVERSE,
                        self,
                        Direccio.DALT,
                        AccionsRana.MOURE,
                    )
                )

            if pos_actual[1] > 1:
                new_pos = (pos_actual[0], pos_actual[1] - 2)
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(
                        Estado(
                            hijo,
                            self.__coste + self.COSTE_SALTAR,
                            self,
                            Direccio.DALT,
                            AccionsRana.BOTAR,
                        )
                    )

        if pos_actual[1] < self.__max_tablero:
            # movimientos hacia abajo
            new_pos = (pos_actual[0], pos_actual[1] + 1)
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(
                    Estado(
                        hijo,
                        self.__coste + self.COSTE_MOVERSE,
                        self,
                        Direccio.BAIX,
                        AccionsRana.MOURE,
                    )
                )

            if pos_actual[1] < self.__max_tablero - 1:
                new_pos = (pos_actual[0], pos_actual[1] + 2)
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(
                        Estado(
                            hijo,
                            self.__coste + self.COSTE_SALTAR,
                            self,
                            Direccio.BAIX,
                            AccionsRana.BOTAR,
                        )
                    )

        return hijos


class RanaEstrella(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__abiertos = None
        self.__cerrados = None
        self.__acciones = None
        self.__saltando = 0

    def _buscar(self, estado: Estado, nombre_rana: str) -> bool:
        """Método que implementa el algoritmo de búsqueda A*.

        Args:
            estado (Estado): Estado en el que se encuentra la rana.
            nombre_rana (str): Nombre de la rana.

        Returns:
            bool: True si ha encontrado la solución, False en caso contrario.
        """
        self.__abiertos = PriorityQueue()
        self.__cerrados = set()

        self.__abiertos.put((estado.calcular_heuritica(nombre_rana), estado))
        estado_actual: Estado = None

        while not self.__abiertos.empty():
            estado_actual = self.__abiertos.get()[1]

            if estado_actual in self.__cerrados:
                continue

            if estado_actual.es_meta(nombre_rana):
                break

            estados_hijos = estado_actual.generar_hijos(nombre_rana)

            for estado_hijo in estados_hijos:
                self.__abiertos.put(
                    (estado_hijo.calcular_heuritica(nombre_rana), estado_hijo)
                )

            self.__cerrados.add(estado_actual)

        if estado_actual.es_meta(nombre_rana):
            acciones = []
            iterador = estado_actual

            acciones.append((iterador.get_accion(), iterador.get_direccion()))
            while iterador.padre is not None:
                accion: Estado = iterador.padre

                # accion, direccion
                acciones.append((accion.get_accion(), accion.get_direccion()))

                iterador = iterador.padre

            self.__acciones = acciones
            return True

        return False

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        # Estado inicial de la rana
        estado_inicial = Estado(
            percep.to_dict(),
            0,
            padre=None,
            accion=AccionsRana.ESPERAR,
            direccion=None,
        )
        print("Inicio test rendimiento")
        start = time.time()
        self._buscar(estado_inicial, "Miquel")
        end = time.time()
        print("Fin test rendimiento")
        print(f"Tiempo de ejecución: {end - start}")
        sys.exit(0)
