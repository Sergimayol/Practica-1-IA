import random
from agent import Rana
from ia_2022 import entorn
from practica1.entorn import AccionsRana, ClauPercepcio, Direccio
import copy


class Individuo:
    def __init__(
        self,
        posicion: tuple = None,
        direccion: Direccio = None,
        padres=None,
        poscion_meta: tuple = None,
    ):
        self.__posicion = posicion
        self.__direccion = direccion
        self.__padres = padres
        self.__poscion_meta = poscion_meta
        self.__fitness = 0

    def __str__(self) -> str:
        return f"Individuo: {self.__posicion} {self.__direccion} {self.__padres} {self.__poscion_meta} {self.__fitness}"

    def __hash__(self):
        return hash(tuple(self.__posicion))

    def __eq__(self, __o: object) -> bool:
        return self.__posicion == __o.__posicion

    def __lt__(self, __o: object) -> bool:
        return self.__fitness < __o.__fitness

    def cruzar(self, otro):
        pass

    def mutar(self):
        pass

    def calcular_fitness(self):
        pass


class RanaGenetica(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        # Class to implement genetic algorithm
        self.__poblacion = None
        self.__acciones = None

    def _buscar(self, estado):
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

    def _generar_poblacion(self, estado):
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
        individuo_inicial = Individuo(
            posicion=percep.posicio,
            direccion=percep.direccio,
            padres=None,
            poscion_meta=percep.meta,
        )

        if self.__acciones is None:
            self._buscar(individuo_inicial)
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
