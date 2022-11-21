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

    def get_frog_names(self) -> list[str]:
        return list(self.__info.get(ClauPercepcio.POSICIO).keys())

    def legal(self, pos_actual: tuple) -> bool:
        # obtener los muros
        walls = self.__info.get(ClauPercepcio.PARETS)
        # comprobar si la posicion actual esta en los muros
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

    def _punto(self, nombre_rana) -> int:
        pos_comida = self.get_comida()
        pos_rana = self.get_posicion(nombre_rana)
        return abs(pos_comida[0] - pos_rana[0]) + abs(pos_comida[1] - pos_rana[1])

    def puntuacion(self, nombre_rana: str) -> int:
        nombres = self.get_frog_names()

        resultado1 = self._punto(nombres[1]) - self._punto(nombres[0])
        resultado2 = self._punto(nombres[0]) - self._punto(nombres[1])

        return resultado1 if nombre_rana == nombres[0] else resultado2


class RanaMiniMax(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)

        self.__saltando = False

    def pinta(self, display):
        pass

    def busqueda_minimax(
        self, estado: Estado, turno: bool = True, recursividad: int = 2
    ):
        """Algoritmo de busqueda minimax
        Min -> False
        Args:
            estado (Estado): Estado inicial del problema
            turno (bool, optional): Turno de la rana. Defaults to True. Min -> False, Max -> True
        Returns:
            int: Valor de la mejor accion
        """
        puntuacion = estado.puntuacion(self.nom)
        if recursividad == 0 or estado.es_meta(self.nom):
            return puntuacion, estado

        estados_hijos = [
            self.busqueda_minimax(estat_fill, not turno, recursividad - 1)
            for estat_fill in estado.generar_hijos(self.nom)
        ]

        return max(estados_hijos) if turno else min(estados_hijos)

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
        resultado = self.busqueda_minimax(estado_inicial)
        iterador = resultado[1]
        accion: Estado = iterador.padre
        iterador = iterador.padre

        if accion is None:
            return AccionsRana.ESPERAR

        if self.__saltando > 0:
            self.__saltando -= 1
            return AccionsRana.ESPERAR

        posicion = (
            estado_inicial.get_posicion(self.nom)[0] - estado_inicial.get_comida()[0],
            estado_inicial.get_posicion(self.nom)[1] - estado_inicial.get_comida()[1],
        )

        posiciones_posibles_finales = {
            (0, 1): (AccionsRana.MOURE, Direccio.DALT),
            (0, -1): (AccionsRana.MOURE, Direccio.BAIX),
            (1, 0): (AccionsRana.MOURE, Direccio.DRETA),
            (-1, 0): (AccionsRana.MOURE, Direccio.ESQUERRE),
        }

        posiciones_posibles_finales2 = {
            (0, 2): (AccionsRana.BOTAR, Direccio.DALT),
            (0, -2): (AccionsRana.BOTAR, Direccio.BAIX),
            (2, 0): (AccionsRana.BOTAR, Direccio.DRETA),
            (-2, 0): (AccionsRana.BOTAR, Direccio.ESQUERRE),
        }

        aux = posiciones_posibles_finales2.get(posicion)
        if aux is not None:
            return aux

        aux = posiciones_posibles_finales.get(posicion)
        if aux is not None:
            return aux

        if accion[0] == AccionsRana.BOTAR:
            self.__saltando = 2
            return accion.get_accion(), accion.get_direccion()

        return accion.get_accion(), accion.get_direccion()
