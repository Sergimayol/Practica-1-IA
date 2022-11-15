import random
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

    def get_fitness(self, nombre_rana: str) -> int:
        # obtener la posicion de la rana
        pos_rana = self.__info.get(ClauPercepcio.POSICIO).get(nombre_rana)
        # obtener la posicion del olor
        pos_olor = self.__info.get(ClauPercepcio.OLOR)
        # calcular la distancia de Manhattan
        return (
            abs(pos_rana[0] - pos_olor[0])
            + abs(pos_rana[1] - pos_olor[1])
            + self.__coste
        )

    @property
    def info(self):
        return self.__info

    def es_meta(self, nombre_rana: str) -> bool:
        return self.__info.get(ClauPercepcio.POSICIO).get(
            nombre_rana
        ) == self.__info.get(ClauPercepcio.OLOR)

    def get_len_tablero(self) -> int:
        return self.__max_tablero

    def set_direccion(self, direccion: Direccio):
        self.__direccion = direccion

    def set_accion(self, accion: AccionsRana):
        self.__accion = accion

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
        return f"Estado: {self.__info}, Coste: {self.__coste}, Accion: {self.__accion}, Direccion: {self.__direccion}"

    def __eq__(self, __o: object) -> bool:
        return self.__info.get(ClauPercepcio.POSICIO) == __o.info.get(
            ClauPercepcio.POSICIO
        )

    def __lt__(self, __o: object) -> bool:
        return False
        # return self.__coste < __o.get_coste()

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
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(
                    Estado(
                        hijo,
                        self.COSTE_MOVERSE,
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
                            self.COSTE_SALTAR,
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
                        self.COSTE_MOVERSE,
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
                            self.COSTE_SALTAR,
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
                        hijo, self.COSTE_MOVERSE, self, Direccio.DALT, AccionsRana.MOURE
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
                            self.COSTE_SALTAR,
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
                        hijo, self.COSTE_MOVERSE, self, Direccio.BAIX, AccionsRana.MOURE
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
                            self.COSTE_SALTAR,
                            self,
                            Direccio.BAIX,
                            AccionsRana.BOTAR,
                        )
                    )

        return hijos


class RanaGenetica(Rana):

    POBLACION_INICIAL = 1000
    NUM_GENERACIONES = 1000

    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        # Class to implement genetic algorithm
        self.__poblacion = None
        self.__acciones = None

    def _buscar(self, estado: Estado):
        """Método que implementa el algoritmo genético.

        Args:
            estado (Estado): Estado inicial del problema.
        """
        # Genetic algorithm
        # 1. Generate initial population with random candidate solutions
        self._generar_poblacion(estado)
        print("Población inicial generada")
        for p in self.__poblacion:
            print(p)
        # 2. Evaluate each candidate
        # self._evaluar_poblacion()
        # 3. Repeat until a solution is found
        while True:
            # 4. Select parents
            padres = self._seleccion()
            # 5. Recombine pair of parents
            self._recombinar(padres)
            # 6. Mutate
            self._mutar()
            # 7. Select individuals for next generation
            self.__poblacion = self._best_individuals()
            # 8. Check if solution is found
            if self._solucion_encontrada():
                break

        # Iterar sobre el estado solución para obtener la secuencia de acciones

    def _best_individuals(self):
        """Select the best individuals to the next generation.

        Returns:
            list: List of best individuals.
        """
        pass

    def _generar_poblacion(self, estado: Estado):
        """Genera la población inicial.

        Args:
            estado (Estado): Estado inicial del problema.
        """
        self.__poblacion = []
        estado_hijo = estado.generar_hijos("Miquel")

        for estado in estado_hijo:
            self.__poblacion.append(estado)

    def _evaluar_poblacion(self):
        """Evalua la población."""
        for estado in self.__poblacion:
            pass

    def _seleccion(self, nombre_rana: str) -> list:
        """Selecciona a los mejores individuos de la población."""
        padres = []
        # Select parents with best fitness
        for individuo in self.__poblacion:
            if len(padres) < 3:
                padres.append(individuo)
            else:
                if individuo.get_fitness(nombre_rana) < padres[0].get_fitness(
                    nombre_rana
                ):
                    padres[0] = individuo
                    continue

                if individuo.get_fitness(nombre_rana) < padres[1].get_fitness(
                    nombre_rana
                ):
                    padres[1] = individuo
                    continue

                if individuo.get_fitness(nombre_rana) < padres[2].get_fitness(
                    nombre_rana
                ):
                    padres[2] = individuo
                    continue

        return padres

    def _recombinar(self, padres: list):
        """Recombina los padres."""
        mejor_padre = padres[0]
        for padre in padres:
            # get the best parent
            if padre.get_fitness("Miquel") > mejor_padre.get_fitness("Miquel"):
                mejor_padre = padre

        # Recombine parents
        self.__poblacion = []
        pass

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

        if self.__acciones is None:
            self._buscar(estado_inicial)
            print("Acciones: ", self.__acciones)

        if len(self.__acciones) == 0:
            return AccionsRana.ESPERAR

        if self.__saltando > 0:
            self.__saltando -= 1
            return AccionsRana.ESPERAR

        accion = self.__acciones.pop()

        if accion[1] is None:
            return accion[0]

        if accion[0] == AccionsRana.BOTAR:
            self.__saltando = 2
            return accion[0], accion[1]

        return accion[0], accion[1]
