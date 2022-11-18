from queue import PriorityQueue
import random
from agent import Rana
from ia_2022 import entorn
from practica1.entorn import AccionsRana, ClauPercepcio, Direccio
import copy


class Individuo:
    LISTA_ACCIONES = [AccionsRana.BOTAR, AccionsRana.MOURE]
    LISTA_DIRECCIONES = [
        Direccio.BAIX,
        Direccio.DRETA,
        Direccio.DRETA,
        Direccio.ESQUERRE,
    ]
    TAM_TABLERO = 8  # 0..7

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
        self.fitness = self._get_distancia(posicion, objetivo)

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

    def cruzar(self, otro):
        num_hijos = random.randint(0, len(self.acciones))
        hijos = []
        for _ in range(num_hijos):
            random_index = random.randint(0, len(self.acciones))
            # acciones = self.acciones[:random_index] + otro.acciones[random_index:]
            acciones = self.acciones[:random_index]
            acciones.extend(otro.acciones[random_index:])

            print("Acciones del cruze: ", acciones)
            input("Ok?")
            acciones_validas = self._get_lista_acciones_validas(acciones)
            individuo = Individuo(
                acciones=acciones_validas,
                posicion=self.posicion,
                objetivo=self.objetivo,
                paredes=self.paredes,
            )
            print("Despues de cruzar", individuo)
            input("Ok?")
            if random.randint(0, 1) == 1:
                individuo._mutar()

            hijos.append(individuo)

        return hijos

    def _mutar(self) -> None:
        acciones = copy.deepcopy(self.acciones)
        print("Antes de mutar", len(acciones))
        acciones[random.randint(0, len(self.acciones) - 1)] = (
            random.choice(self.LISTA_ACCIONES),
            random.choice(self.LISTA_DIRECCIONES),
        )
        self.acciones = acciones

    def calcular_fitness(self):
        """Función de fitness: El fitness de un individuo vendrá dado por la
        distancia que le queda al individuo para llegar a la meta, desde su
        última acción.
        """
        pos_actual = self.posicion
        pos_siguiente = None

        for accion in self.acciones:
            pos_siguiente = self._get_posicion_siguiente(pos_actual, accion)
            self.fitness = self._get_distancia(pos_siguiente, self.objetivo)

    def _get_distancia(self, pos1: tuple, pos2: tuple) -> int:
        """Calcula la distancia entre dos posiciones

        Arguments:
            pos1 {tuple} -- Posición 1\n
            pos2 {tuple} -- Posición 2

        Returns:
            int -- Distancia entre las dos posiciones
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def generar_acciones_aleatorias(self):
        """
        Genera una lista de acciones aleatorias, donde cada acción es
        un movimiento válido.
        """
        acciones = []
        num_acciones = random.randint(1, 12)
        for _ in range(num_acciones):
            acciones.append(
                (
                    random.choice(self.LISTA_ACCIONES),
                    random.choice(self.LISTA_DIRECCIONES),
                )
            )
        # Cortar la lista de acciones si encuentra una acción que no es válida,
        #  para quedarse con los primeros movimientos válidos
        self.acciones = self._get_lista_acciones_validas(acciones)

    def generar_poblacion_incial(self, num_individuos: int):
        poblacion = []
        for _ in range(num_individuos):
            acciones = []
            num_acciones = random.randint(0, 20)
            # acciones.append(self.acciones)
            for _ in range(num_acciones):
                acciones.append(
                    (
                        random.choice(self.LISTA_ACCIONES),
                        random.choice(self.LISTA_DIRECCIONES),
                    )
                )

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
        pos_actual = self.posicion
        nueva_lista_acciones = []
        # Recorrer la lista de acciones hasta encontrar una acción que no sea válida
        for accion in acciones:
            pos_actual = self._get_posicion_siguiente(pos_actual, accion)
            if not self._es_posicion_valida(pos_actual):
                nueva_lista_acciones = acciones[: acciones.index(accion)]
                break

        return nueva_lista_acciones

    def _get_posicion_siguiente(
        self, pos_actual: tuple, accion_a_realizar: tuple
    ) -> tuple:
        accion, direccion = accion_a_realizar

        # Desplazamiento -> Botar(2) o Mover(1)
        desplazamiento = 1 if accion == AccionsRana.MOURE else 2

        if direccion == Direccio.ESQUERRE:  # Izquierda
            return (pos_actual[0] - desplazamiento, pos_actual[1])

        if direccion == Direccio.DRETA:  # Derecha
            return (pos_actual[0] + desplazamiento, pos_actual[1])

        if direccion == Direccio.BAIX:  # Abajo
            return (pos_actual[0], pos_actual[1] + desplazamiento)

        if direccion == Direccio.DALT:  # Arriba
            return (pos_actual[0], pos_actual[1] - desplazamiento)

    def _es_posicion_valida(self, pos: tuple) -> bool:
        return (
            pos[0] >= 0
            and pos[0] < self.TAM_TABLERO
            and pos[1] >= 0
            and pos[1] < self.TAM_TABLERO
            and pos not in self.paredes
        )


class RanaGenetica(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__acciones = None
        self.__saltando = 0

    def _busquedaGenetica(self, individuo: Individuo):
        poblacion = individuo.generar_poblacion_incial(50)
        cola = PriorityQueue()

        for individuo in poblacion:
            individuo.calcular_fitness()
            print(individuo)
            cola.put(individuo)

        input("Pulsa enter para continuar")

        while len(poblacion) > 0:
            print("Inicio de iteración")
            print("Poblacion: ", len(poblacion))
            for _ in range(10):
                individuo1 = cola.get()
                individuo2 = cola.get()

                print("Individuo 1: ", individuo1)
                print("Individuo 2: ", individuo2)
                input("Pulsa enter para continuar")

                poblacion.extend(individuo1.cruzar(individuo2))

                for individuo in poblacion:
                    individuo.calcular_fitness()
                    print("Individuo en población despues de cruze", individuo)
                    cola.put(individuo)

                for individuo in cola.queue:
                    print(individuo.fitness)
                    if individuo.es_meta():
                        self.__acciones = individuo.acciones
                        return True

        return False

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        # Estado inicial de la rana
        percepciones = percep.to_dict()

        individuo = Individuo(
            acciones=[percepciones[ClauPercepcio.POSICIO].get("Miquel")],
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
