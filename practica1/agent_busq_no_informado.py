from agent import Rana
from practica1.agent import Estado
from ia_2022 import entorn
from practica1 import entorn as entorn_practica1


class RanaBusquedaNoInformada(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__abiertos = None
        self.__cerrados = None
        self.__acciones = None

    def _buscar(self, estado: Estado, profundidad: int = 5):
        """Método que implementa el algoritmo de búsqueda no informada. Este método
        implementa el algoritmo de búsqueda por profundidad.

        Args:
            estado (Estado): Estado en el que se encuentra la rana.
        """
        #Lista de estados abiertos
        self.__abiertos = []
        #Conjunto de estados cerrados
        self.__cerrados = set()
        #Añadimos el estado inicial a la lista de abiertos
        self.__abiertos.append(estado)
        #Declaramos el estado actual como None
        estado_actual: Estado = None
        #La profundidad actual es igual a la profundidad pasada por parámetro
        profundidad_actual = profundidad
        #Mientras la lista de abiertos no esté vacía y la profundidad actual sea mayor o igual que 0
        while len(self.__abiertos) > 0 and profundidad_actual >= 0:
            #Sacamos el último estado de la lista de abiertos
            estado_actual = self.__abiertos.pop()
            #Si el estado actual está en la lista de cerrados
            if estado_actual in self.__cerrados:
                #Seguimos
                continue
            #Si el estado actual es el estado meta
            if estado_actual.es_meta("Miquel"):
                #Salimos del bucle
                break

            # Se generan los estados hijos del estado actual
            estados_hijos = estado_actual.generar_hijos("Miquel")

            #Para cada estado de los estados hijos
            for estado_hijo in estados_hijos:
                #Añadimos el estado hijo a la lista de abiertos
                self.__abiertos.append(estado_hijo)
            #Añadimos el estado actual a la lista de cerrados
            self.__cerrados.add(estado_actual)
            #Decrementamos la profundidad actual
            profundidad_actual -= 1

        #Control de errores
        if estado_actual is None:
            raise ValueError("Error imposible")

        #Si el estado actual es el estado meta
        if estado_actual.es_meta():
            #Se declara una lista de acciones vacía
            acciones = []
            #Se crea un iterador y pasamos el estado actual
            iterador = estado_actual
            while iterador.padre is not None:
                padre, accion = iterador.padre
                acciones.append(accion)
                iterador = padre

            self.__acciones = acciones
            return True
        acciones = []
        iterador = estado_actual
        while iterador.padre is not None:
            padre, accion = iterador.padre
            acciones.append(accion)
            iterador = padre

        self.__acciones = acciones
        return False

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        # Estado inicial de la rana
        estado_inicial = Estado(percep.to_dict(), 0, padre=None)

        if self.__acciones is None:
            self._buscar(estado_inicial)
            print("Lista de acciones: ", self.__acciones)

        if len(self.__acciones) == 0:
            return entorn_practica1.AccionsRana.ESPERAR

        return entorn_practica1.AccionsRana.BOTAR, self.__acciones.pop()
