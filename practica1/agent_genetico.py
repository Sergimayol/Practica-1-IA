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

    def __init__(self, acciones: list, fitness: float = 0, padre: tuple = None):
        self.acciones = acciones
        self.fitness = fitness
        self.padre = padre

    def cruzar(self, otro):
        random_index = random.randint(0, len(self.acciones) - 1)
        acciones = self.acciones[:random_index] + otro.acciones[random_index:]
        return Individuo(acciones, padre=(self, otro))

    def mutar(self) -> None:
        acciones = copy.deepcopy(self.acciones)
        acciones[random.randint(0, len(acciones) - 1)] = (
            random.choice(self.LISTA_ACCIONES),
            random.choice(self.LISTA_DIRECCIONES),
        )
        self.acciones = acciones

    def calcular_fitness(self):
        pass

    def generar_acciones_aleatorias(self):
        return [
            (random.choice(self.LISTA_ACCIONES), random.choice(self.LISTA_DIRECCIONES))
            for _ in range(8)
        ]


class RanaGenetica(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__acciones = None
        self.__saltando = 0

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        # Estado inicial de la rana
        print(percep)
        individuo = Individuo()
        print(individuo.generar_acciones_aleatorias())
        return AccionsRana.ESPERAR
