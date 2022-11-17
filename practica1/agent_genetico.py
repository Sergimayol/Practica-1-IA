import random
from agent import Rana
from ia_2022 import entorn
from practica1.entorn import AccionsRana, ClauPercepcio, Direccio
import copy


class Individuo:
    def __init__(self, acciones: list, fitness: float = 0, padre=None):
        self.acciones = acciones
        self.fitness = fitness
        self.padre = padre

    def cruzar(self, otro):
        pass

    def mutar(self):
        pass

    def calcular_fitness(self):
        pass

    def generar_acciones_aleatorias(self):
        acciones = [AccionsRana.BOTAR, AccionsRana.ESPERAR, AccionsRana.MOURE]
        direcciones = [Direccio.BAIX, Direccio.DRETA, Direccio.DRETA, Direccio.ESQUERRE]
        return [(random.choice(acciones), random.choice(direcciones)) for _ in range(8)]


class RanaGenetica(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__abiertos = None
        self.__cerrados = None
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
