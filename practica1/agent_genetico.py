from queue import PriorityQueue
import random
from agent import Rana
from ia_2022 import entorn
from practica1.entorn import AccionsRana, ClauPercepcio, Direccio
import copy


class Individuo:
    LISTA_ACCIONES = [AccionsRana.BOTAR, AccionsRana.ESPERAR, AccionsRana.MOURE]
    LISTA_DIRECCIONES = [
        Direccio.BAIX,
        Direccio.DRETA,
        Direccio.DRETA,
        Direccio.ESQUERRE,
    ]

    def __init__(
        self,
        acciones: list,
        fitness: int = 0,
        padre: tuple = None,
        posicion: tuple = None,
        objetivo: tuple = None,
        paredes: list = None,
    ):
        self.acciones = acciones
        self.fitness = fitness
        self.padre = padre
        self.posicion = posicion
        self.objetivo = objetivo
        self.paredes = paredes

    def __str__(self) -> str:
        return f"Individuo: {self.acciones}, Fitness: {self.fitness}, Posicion: {self.posicion}, Objetivo: {self.objetivo}"

    def __eq__(self, other):
        return self.fitness == other.get_valor()

    """"
    Funció per ordenar a la cua de prioritat segons la fitness de l'individu
    """

    def __lt__(self, other):
        return self.fitness < other.get_valor()

    def get_valor(self):
        return self.fitness

    def __hash__(self):
        return hash(tuple(self.posicion))

    def get_pos_ag(self):
        return self.posicion

    def cruzar(self, otro):
        random_index = random.randint(0, len(self.acciones) - 1)
        acciones = self.acciones[:random_index] + otro.acciones[random_index:]
        return Individuo(
            acciones, padre=(self, otro), objetivo=self.objetivo, posicion=self.posicion
        )

    def mutar(self) -> None:
        acciones = copy.deepcopy(self.acciones)
        acciones[random.randint(0, len(acciones) - 1)] = (
            random.choice(self.LISTA_ACCIONES),
            random.choice(self.LISTA_DIRECCIONES),
        )
        self.acciones = acciones

    def calcular_fitness(self):
        self.fitness = abs(self.posicion[0] - self.objetivo[0]) + abs(
            self.posicion[1] - self.objetivo[1]
        )

    def generar_acciones_aleatorias(self):
        acciones = []
        for _ in range(8):
            accion_aleratoria = random.choice(self.LISTA_ACCIONES)
            if accion_aleratoria == AccionsRana.ESPERAR:
                acciones.append((accion_aleratoria, None))
            else:
                acciones.append(
                    (accion_aleratoria, random.choice(self.LISTA_DIRECCIONES))
                )
        self.acciones = acciones


class RanaGenetica(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__acciones = None
        self.__saltando = 0

    def _busquedaGenetica(self, individuo: Individuo):
        # Creamos la población inicial
        poblacion = []
        for _ in range(10):
            individuo.generar_acciones_aleatorias()
            poblacion.append(individuo)

        # Evaluamos la población
        for individuo in poblacion:
            individuo.calcular_fitness()

        # Ordenamos la población
        queue = PriorityQueue()  # Los individuos con mejor fitness van al principio
        for individuo in poblacion:
            queue.put(individuo)

        while len(poblacion) > 0:
            print("Poblacion: ", len(poblacion))
            for _ in range(10):
                # Seleccionamos los dos mejores individuos
                individuo1 = queue.get()
                individuo2 = queue.get()

                # Cruzamos los dos individuos
                individuo_hijo = individuo1.cruzar(individuo2)

                # Mutamos el individuo hijo
                individuo_hijo.mutar()

                # Calculamos el fitness del individuo hijo
                individuo_hijo.calcular_fitness()

                # Añadimos el individuo hijo a la población
                poblacion.append(individuo_hijo)

                # Añadimos el individuo hijo a la cola de prioridad
                queue.put(individuo_hijo)

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
            None,
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
