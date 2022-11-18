from agent import Rana, Estado
from ia_2022 import entorn
from practica1 import joc, entorn as entorn_practica1
from practica1.entorn import AccionsRana, ClauPercepcio, Direccio
import copy
import os


class Estado:
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

    def get_coste(self) -> int:
        return self.__coste

    def get_accion(self) -> AccionsRana or None:
        return self.__accion

    @property
    def info(self):
        return self.__info

    def es_meta(self, nombre_rana: str) -> bool:
        return self.__info.get(ClauPercepcio.POSICIO).get(
            nombre_rana
        ) == self.__info.get(ClauPercepcio.OLOR)

    def get_posicion(self, nombre_rana: str) -> tuple:
        return self.__info.get(ClauPercepcio.POSICIO).get(nombre_rana)

    def get_comida(self):
        return self.__info.get(ClauPercepcio.OLOR)

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
        return (
            str(self.__info)
            + f" coste: {self.__coste}"
            + f" accion: {self.__accion}"
            + f" direccion: {self.__direccion}"
        )

    def __eq__(self, __o: object) -> bool:
        return self.__info.get(ClauPercepcio.POSICIO) == __o.info.get(
            ClauPercepcio.POSICIO
        )

    def __lt__(self, __o: object) -> bool:
        return False
        # return self.__coste < __o.get_coste()

    def calcular_heuritica(self, nombre_rana) -> int:
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

        hijos = []

        # pos 0 = x, pos 1 = y (empiezan en 0)
        pos_actual = self.__info.get(ClauPercepcio.POSICIO).get(nombre_rana)
        if pos_actual[0] > 0:
            # movimientos a la izquierda
            new_pos = (pos_actual[0] - 1, pos_actual[1])
            # Estado hijo a crear
            estado_hijo: Estado = None
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                estado_hijo = Estado(
                    hijo, self.__coste + 1, self, Direccio.ESQUERRE, AccionsRana.MOURE
                )

            if pos_actual[0] > 1:
                new_pos = (pos_actual[0] - 2, pos_actual[1])
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    estado_hijo = Estado(
                        hijo,
                        self.__coste + 2,
                        self,
                        Direccio.ESQUERRE,
                        AccionsRana.BOTAR,
                    )
            if estado_hijo is not None:
                hijos.append(estado_hijo)

        if pos_actual[0] < self.__max_tablero:
            # movimientos a la derecha
            new_pos = (pos_actual[0] + 1, pos_actual[1])
            # Estado hijo a crear
            estado_hijo: Estado = None
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                estado_hijo = Estado(
                    hijo, self.__coste + 1, self, Direccio.DRETA, AccionsRana.MOURE
                )

            if pos_actual[0] < self.__max_tablero - 1:
                new_pos = (pos_actual[0] + 2, pos_actual[1])
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    estado_hijo = Estado(
                        hijo,
                        self.__coste + 2,
                        self,
                        Direccio.DRETA,
                        AccionsRana.BOTAR,
                    )

            if estado_hijo is not None:
                hijos.append(estado_hijo)

        if pos_actual[1] > 0:
            # movimientos hacia arriba
            new_pos = (pos_actual[0], pos_actual[1] - 1)
            # Estado hijo a crear
            estado_hijo: Estado = None
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                estado_hijo = Estado(
                    hijo, self.__coste + 1, self, Direccio.DALT, AccionsRana.MOURE
                )

            if pos_actual[1] > 1:
                new_pos = (pos_actual[0], pos_actual[1] - 2)
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    estado_hijo = Estado(
                        hijo, self.__coste + 2, self, Direccio.DALT, AccionsRana.BOTAR
                    )

            if estado_hijo is not None:
                hijos.append(estado_hijo)

        if pos_actual[1] < self.__max_tablero:
            # movimientos hacia abajo
            new_pos = (pos_actual[0], pos_actual[1] + 1)
            # Estado hijo a crear
            estado_hijo: Estado = None
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                estado_hijo = Estado(
                    hijo, self.__coste + 1, self, Direccio.BAIX, AccionsRana.MOURE
                )

            if pos_actual[1] < self.__max_tablero - 1:
                new_pos = (pos_actual[0], pos_actual[1] + 2)
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    estado_hijo = Estado(
                        hijo, self.__coste + 2, self, Direccio.BAIX, AccionsRana.BOTAR
                    )

            if estado_hijo is not None:
                hijos.append(estado_hijo)
        return hijos

    def punto(self, nombre_rana):
        pos_comida = self.get_comida()
        pos_rana = self.get_posicion(nombre_rana)
        punto = abs(pos_comida[0] - pos_rana[0]) + abs(pos_comida[1] - pos_rana[1])
        return punto

    def puntuacion(self, nombre_rana: str) -> int:
        if nombre_rana == "Miquel":
            return self.punto("Pep") - self.punto("Miquel")
        else:
            return self.punto("Miquel") - self.punto("Pep")


class RanaMiniMax(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)

        self.__saltando = False

    def pinta(self, display):
        pass

    def busqueda_minimax(self, estado: Estado, turno: bool, recursividad: int):
        """Algoritmo de busqueda minimax
        Min -> False
        Args:
            estado (Estado): Estado inicial del problema
            turno (bool, optional): Turno de la rana. Defaults to True. Min -> False, Max -> True
        Returns:
            int: Valor de la mejor accion
        """
        puntuacion = estado.puntuacion(self.nom)
        if recursividad == 2 or estado.es_meta(self.nom):
            return puntuacion, estado

        # [print(self.minimax(estat_fill, not turno_max, recursividad + 1)) for estat_fill in estat.genera_fills()]
        point_fills = [
            self.busqueda_minimax(estat_fill, not turno, recursividad + 1)
            for estat_fill in estado.generar_hijos(self.nom)
        ]
        # print(punto)
        if turno:
            return max(point_fills)
        else:
            return min(point_fills)

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        # Estado inicial de la rana
        estado_inicial = Estado(
            percep.to_dict(),
            0,
            padre=None,
            direccion=None,
            accion=AccionsRana.ESPERAR,
        )
        # Devuelve puntuacion y estado
        resultado = self.busqueda_minimax(estado_inicial, turno=True, recursividad=0)
        iterador = resultado[1]

        ultima_accion = (iterador.get_accion(), iterador.get_direccion())
        accion: Estado = iterador.padre
        iterador = iterador.padre

        if self.__saltando > 0:
            self.__saltando -= 1
            return AccionsRana.ESPERAR

        posicion = abs(
            estado_inicial.get_posicion(self.nom)[0] - estado_inicial.get_comida()[0]
        ) + abs(
            estado_inicial.get_posicion(self.nom)[1] - estado_inicial.get_comida()[1]
        )

        if posicion <= 2:
            return ultima_accion

        if accion[0] == AccionsRana.BOTAR:
            self.__saltando = 2
            return accion.get_accion(), accion.get_direccion()

        return accion.get_accion(), accion.get_direccion()
