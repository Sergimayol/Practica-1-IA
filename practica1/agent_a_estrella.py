from queue import PriorityQueue
from agent import Rana
from practica1.agent import Estado
from ia_2022 import entorn
from practica1 import entorn as entorn_practica1


class RanaEstrella(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__abiertos = None
        self.__cerrados = None
        self.__acciones = None

    def _buscar(self, estado: Estado):
        self.__abiertos = PriorityQueue()
        self.__cerrados = set()

        print("Estado inicial: ", estado)
        print("Heurística: ", estado.calcular_heuritica("Miquel"))
        self.__abiertos.put((estado.calcular_heuritica("Miquel"), estado))
        estado_actual: Estado = None
        while not self.__abiertos.empty():
            estado_actual = self.__abiertos.get()[1]

            if estado_actual in self.__cerrados:
                continue

            if estado_actual.es_meta("Miquel"):
                break

            estados_hijos = estado_actual.generar_hijos("Miquel")

            for estado_hijo in estados_hijos:
                self.__abiertos.put(
                    (estado_hijo.calcular_heuritica("Miquel"), estado_hijo)
                )

            self.__cerrados.add(estado_actual)

            if estado_actual.es_meta("Miquel"):
                accions = []
                iterador = estado_actual

                while iterador.padre is not None:
                    pare, accio = iterador.padre

                    accions.append(accio)
                    iterador = pare
                self.__acciones = accions

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        estado_inicial = Estado(percep.to_dict(), 0, padre=None)

        if self.__acciones is None:
            self._buscar(estado_inicial)

        if self.__acciones:
            acc = self.__acciones.pop()

            return acc[0], acc[1]

        return entorn_practica1.AccionsRana.ESPERAR
