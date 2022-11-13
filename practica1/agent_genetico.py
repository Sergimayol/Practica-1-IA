from agent import Rana
from practica1.agent import Estado
from ia_2022 import entorn
from practica1 import entorn as entorn_practica1


class RanaGenetica(Rana):
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
        # 1. Generate initial population
        self._generar_poblacion(estado)
        while True:
            # 2. Evaluate population
            self._evaluar_poblacion()
            # 3. Select individuals
            self._seleccion()
            # 4. Create new population
            self._crear_poblacion()
            # 5. Check if solution is found
            if self._solucion_encontrada():
                break
        # 6. Repeat steps 2 to 5 until a solution is found
        pass

    def _generar_poblacion(self, estado: Estado):
        """Método que genera la población inicial.

        Args:
            estado (Estado): Estado inicial del problema.
        """
        pass

    def _evaluar_poblacion(self):
        """Método que evalúa la población."""
        pass

    def _fitness(self, individuo):
        """Método que calcula el fitness de un individuo.

        Args:
            individuo (list): Individuo del que se quiere calcular el fitness.

        Returns:
            float: Fitness del individuo.
        """
        pass

    def _seleccion(self, poblacion):
        """Método que implementa la selección de los individuos de la población.

        Args:
            poblacion (list): Población de la que se quiere seleccionar los individuos.

        Returns:
            list: Individuos seleccionados.
        """
        pass

    def _cruce(self, individuo1, individuo2):
        """Método que implementa el cruce de dos individuos.

        Args:
            individuo1 (list): Primer individuo.
            individuo2 (list): Segundo individuo.

        Returns:
            list: Individuo resultante del cruce.
        """
        pass

    def _mutacion(self, individuo):
        """Método que implementa la mutación de un individuo.

        Args:
            individuo (list): Individuo que se quiere mutar.

        Returns:
            list: Individuo mutado.
        """
        pass

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        # Estado inicial de la rana
        estado_inicial = Estado(percep.to_dict(), 0, padre=None)

        return entorn_practica1.AccionsRana.ESPERAR
