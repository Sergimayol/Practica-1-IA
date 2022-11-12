from agent import Rana
from practica1.agent import Estado
from practica1.entorn import ClauPercepcio, AccionsRana, Direccio
from queue import PriorityQueue
from ia_2022 import entorn
from practica1 import entorn as entorn_practica1

class RanaEstrella(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__abiertos = None
        self.__cerrados = None
        self.__acciones = None
    

    def _buscar(self, estado: Estado):
        # Inicializamos la lista de abiertos como una cola de prioridad
        self.__abiertos = PriorityQueue()
        # Inicializamos la lista de cerrados como un conjunto
        self.__cerrados = set()
        # Añadimos el estado inicial a la lista de abiertos y calculamos la heurística
        self.__abiertos.put((estado.calcula_heuristica(), estado))
        # Declaramos el estado actual como None
        estado_actual = None
        
        # Mientras la lista de abiertos no esté vacía
        while len(self.__abiertos) > 0:
            # Sacamos el último estado de la lista de abiertos
            estado_actual = self.__abiertos.get()
            
            if estado_actual in self.__cerrados:
                continue
            if estado_actual.es_meta("Miquel"):
                break
            
            estados_hijos = estado_actual.generar_hijos("Miquel")

            for estado_hijo in estados_hijos:
                self.__abiertos.put((estado_hijo.calcula_heuristica(), estado_hijo))
            self.__cerrados.add(estado_actual)
        
        if estado_actual is None:
            raise ValueError("Error imposible")
        
        if estado_actual.es_meta("Miquel"):
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
