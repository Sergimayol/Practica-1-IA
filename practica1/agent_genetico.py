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
    TAM_TABLERO = 7  # 0..7

    def __init__(
        self,
        acciones: list,
        fitness: int = 0,
        posicion: tuple = None,
        objetivo: tuple = None,
        paredes: list = None,
    ):
        self.acciones = acciones
        self.fitness = fitness
        self.posicion = posicion
        self.objetivo = objetivo
        self.paredes = paredes

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

    def cruzar(self, otro):
        num_cruces = random.randint(0, len(self.acciones))
        hijos = []
        for _ in range(num_cruces):
            random_index = random.randint(0, len(self.acciones))
            # acciones = self.acciones[:random_index] + otro.acciones[random_index:]
            acciones = self.acciones[:random_index]
            acciones.extend(otro.acciones[random_index:])

            individuo = Individuo(
                acciones=acciones,
                posicion=self.posicion,
                objetivo=self.objetivo,
                paredes=self.paredes,
            )

            print("Acciones del cruze: ", acciones)

            individuo.acciones = self._get_lista_acciones_validas(individuo.acciones)
            print("Despues de cruzar", len(individuo.acciones))
            if random.randint(0, 1) == 1 and len(individuo.acciones) > 0:
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
        self.fitness = abs(self.posicion[0] - self.objetivo[0]) + abs(
            self.posicion[1] - self.objetivo[1]
        )

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
        # Creamos la población inicial
        poblacion = []

        for _ in range(10):
            indv = Individuo(
                acciones=[],
                posicion=individuo.posicion,
                objetivo=individuo.objetivo,
                paredes=individuo.paredes,
            )
            while True:
                indv.generar_acciones_aleatorias()
                if len(indv.acciones) > 0:
                    break
            poblacion.append(indv)
            print("Individuo: ", indv)

        queue = PriorityQueue()  # Los individuos con mejor fitness van al principio

        # Evaluamos y ordenamos la población
        for individuo in poblacion:
            individuo.calcular_fitness()
            queue.put(individuo)

        while len(poblacion) > 0:

            for _ in range(10):
                # Seleccionamos los dos mejores individuos
                individuo1 = queue.get()
                individuo2 = queue.get()

                print("Individuo 1: ", individuo1)
                print("Individuo 2: ", individuo2)

                # Cruzamos los individuos
                while True:
                    hijos = individuo1.cruzar(individuo2)
                    if len(hijos) > 0:
                        break

                print("Hijos generados del cruze: ", hijos)

                # Aumentamos la población con los mejores individuos
                poblacion.extend(hijos)

                # Evaluamos y ordenamos la población
                for individuo in poblacion:
                    individuo.calcular_fitness()
                    queue.put(individuo)

                # Comprobamos si alguno de los individuos es el objetivo
                for individuo in queue.queue:
                    if individuo.get_valor() == 0:
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
