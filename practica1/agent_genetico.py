from queue import PriorityQueue
import random
from agent import Rana
from ia_2022 import entorn
from practica1.entorn import AccionsRana, ClauPercepcio, Direccio
import copy


class Individuo:
    LISTA_ACCIONES = [
        (0, +1),
        (0, -1),
        (+1, 0),
        (-1, 0),
        (0, +2),
        (0, -2),
        (+2, 0),
        (-2, 0),
    ]
    MAPA_ACCIONES_DIRECCIONES = {
        (0, +1): (AccionsRana.MOURE, Direccio.BAIX),
        (0, -1): (AccionsRana.MOURE, Direccio.DALT),
        (+1, 0): (AccionsRana.MOURE, Direccio.DRETA),
        (-1, 0): (AccionsRana.MOURE, Direccio.ESQUERRE),
        (0, +2): (AccionsRana.BOTAR, Direccio.BAIX),
        (0, -2): (AccionsRana.BOTAR, Direccio.DALT),
        (+2, 0): (AccionsRana.BOTAR, Direccio.DRETA),
        (-2, 0): (AccionsRana.BOTAR, Direccio.ESQUERRE),
    }
    TAM_TABLERO = 8  # Tamaño del tablero

    def __init__(
        self,
        acciones: list,
        fitness: int = 0,
        posicion: tuple = None,
        objetivo: tuple = None,
        paredes: list = None,
    ):
        self.acciones = acciones
        self.posicion = posicion
        self.objetivo = objetivo
        self.paredes = paredes
        self.fitness = fitness

    def __str__(self) -> str:
        return f"Acciones: {self.acciones}, Fitness: {self.fitness}, Posicion: {self.posicion}, Objetivo: {self.objetivo}"

    def __eq__(self, other):
        return self.fitness == other.get_valor()

    def __lt__(self, other):
        return self.fitness < other.get_valor()

    def get_valor(self):
        return self.fitness

    def __hash__(self):
        return hash(tuple(self.posicion))

    def get_pos_ag(self):
        return self.posicion

    def es_meta(self):
        return self.fitness == 0

    def cruzar(self, otro) -> list:
        """Cruza dos individuos, generando una cantidad aleatoria de hijos entre
        cero y la longitud de las acciones a realizar.

        Args:
            otro (Individuo): Individuo con el que se cruzará.

        Returns:
            hijos (list): Lista de hijos generados en el cruce.
        """
        hijos = []
        num_hijos = random.randint(0, len(self.acciones))

        for _ in range(num_hijos):
            indice_de_corte = random.randint(0, len(self.acciones))
            parte1 = self.acciones[:indice_de_corte]
            parte2 = otro.acciones[indice_de_corte:]

            parte1.extend(parte2)

            acciones_generadas_validas = self._get_lista_acciones_validas(parte1)

            hijo = Individuo(
                acciones=acciones_generadas_validas,
                posicion=self.posicion,
                objetivo=self.objetivo,
                paredes=self.paredes,
            )

            # Mutar -> prob (50%)
            if random.randint(0, 1) == 0:
                hijo._mutar()

            hijos.append(hijo)

        return hijos

    def _mutar(self) -> None:
        """Realiza una mutación en el individuo, cambiando una acción aleatoria
        por otra aleatoria. Posibles mutaciones:
            - Cambiar una acción.
            - Añadir una acción.
        """
        if random.randint(0, 1) == 0:
            # Cambiar una acción
            indice = random.randint(0, len(self.acciones) - 1)
            self.acciones[indice] = random.choice(self.LISTA_ACCIONES)
        else:
            # Añadir una acción
            self.acciones.append(random.choice(self.LISTA_ACCIONES))

    def calcular_fitness(self):
        """Función de fitness: El fitness de un individuo vendrá dado por la
        distancia que le queda al individuo para llegar a la meta, desde su
        última acción.
        """
        pos_actual = (0, 0)

        for e in self.acciones:
            pos_final = self._get_posicion_siguiente(pos_actual, e)
            pos_actual = pos_final

        self.fitness = self._get_distancia(pos_final, self.objetivo)

    def _get_distancia(self, pos1: tuple, pos2: tuple) -> int:
        """Calcula la distancia entre dos posiciones

        Arguments:
            pos1 {tuple} -- Posición 1\n
            pos2 {tuple} -- Posición 2

        Returns:
            int -- Distancia entre las dos posiciones
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def generar_poblacion_incial(self, num_individuos: int) -> list:
        """Genera una población inicial de individuos, donde todas serán acciones
        válidas. Cada una de las acciones será una lista de acciones aleatorias
        válidas comenzando desde la posición actual del individuo.

        Args:
            num_individuos (int): Número de individuos que incialamente forman la
            población.

        Returns:
            poblacion (list): Lista de individuos.
        """
        poblacion = []
        for _ in range(num_individuos):
            acciones = []
            num_acciones = random.randint(0, 20)
            acciones.append(self.acciones)
            for _ in range(num_acciones):
                acciones.append(random.choice(self.LISTA_ACCIONES))

            acciones_validas = self._get_lista_acciones_validas(acciones)

            indiv = Individuo(
                acciones=acciones_validas,
                posicion=self.posicion,
                objetivo=self.objetivo,
                paredes=self.paredes,
            )

            poblacion.append(indiv)

        return poblacion

    def _get_lista_acciones_validas(self, acciones: list) -> list:
        """Devuelve una lista de acciones válidas

        Arguments:
            acciones {list} -- Lista de acciones

        Returns:
            list -- Lista de acciones válidas
        """
        acciones_validas = []
        pos_actual = (0, 0)
        for accion in acciones:
            pos_siguiente = self._get_posicion_siguiente(pos_actual, accion)

            if not self._es_posicion_valida(pos_siguiente):
                break

            acciones_validas.append(accion)
            pos_actual = pos_siguiente

        return acciones_validas

    def _get_posicion_siguiente(self, pos_actual: tuple, accion: tuple) -> tuple:
        """Devuelve la posición siguiente a partir de una posición actual y una
        acción

        Arguments:
            pos_actual {tuple} -- Posición actual\n
            accion {tuple} -- Acción

        Returns:
            tuple -- Posición siguiente
        """
        return (pos_actual[0] + accion[0], pos_actual[1] + accion[1])

    def _es_posicion_valida(self, pos: tuple) -> bool:
        """Comprueba si una posición es válida

        Arguments:
            pos {tuple} -- Posición a comprobar

        Returns:
            bool -- True si la posición es válida, False en caso contrario
        """
        return (
            0 <= pos[0] < self.TAM_TABLERO
            and 0 <= pos[1] < self.TAM_TABLERO
            and pos not in self.paredes
        )

    def get_acciones_direcciones(self) -> list:
        """Devuelve una lista de acciones en forma de acción - dirección

        Returns:
            acciones_direcciones (list): Lista de acciones en forma de acción - dirección
        """
        acciones_direcciones = []
        lista_acciones = self.acciones[::-1]

        for accion in lista_acciones:
            if not (accion == self.posicion):
                aux = self.MAPA_ACCIONES_DIRECCIONES.get(accion)
                acciones_direcciones.append(aux)

        return acciones_direcciones


class RanaGenetica(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__acciones = None
        self.__saltando = 0

    def _busquedaGenetica(self, individuo: Individuo):
        poblacion = individuo.generar_poblacion_incial(20)
        cola = PriorityQueue()

        for individuo in poblacion:
            individuo.calcular_fitness()
            print(individuo)
            cola.put(individuo)

        while len(poblacion) > 0:

            for _ in range(10):
                individuo1 = cola.get()
                individuo2 = cola.get()

                poblacion.extend(individuo1.cruzar(individuo2))

                for individuo in poblacion:
                    individuo.calcular_fitness()
                    cola.put(individuo)

                for individuo in cola.queue:
                    if individuo.es_meta():
                        print("\n\n")
                        print("Meta")
                        print(individuo)
                        print("\n\n")
                        self.__acciones = individuo.get_acciones_direcciones()
                        return True

        return False

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        # Estado inicial de la rana
        percepciones = percep.to_dict()

        individuo = Individuo(
            acciones=percepciones[ClauPercepcio.POSICIO].get("Miquel"),
            posicion=percepciones[ClauPercepcio.POSICIO].get("Miquel"),
            objetivo=percepciones[ClauPercepcio.OLOR],
            paredes=percepciones[ClauPercepcio.PARETS],
        )

        if self.__acciones is None:
            self._busquedaGenetica(individuo)
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
