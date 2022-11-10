from agent import Rana
from practica1.agent import Estado
from ia_2022 import entorn
from practica1 import entorn as entorn_practica1


class RanaBusquedaNoInformada(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.abiertos = None
        self.cerrados = None
        self.acciones = None

    def _buscar(self, estado: Estado):
        self.abiertos = []
        self.cerrados = set()
        self.abiertos.append(estado)
        actual = None
        while len(self.abiertos) > 0:
            actual = self.abiertos[0]
            self.abiertos = self.abiertos[1:]

            if actual in self.cerrados:
                continue
            estados_hijos = actual.generar_hijos()

            if actual.es_meta():
                break

            for estat_final in estados_hijos:
                self.abiertos.append(estat_final)

            self.cerrados.add(actual)
        if actual is None:
            raise ValueError("Error al buscar")

        if actual.es_meta():
            acciones = []
            iterador = actual

            while iterador.padre() is not None:
                padre, accion = iterador.padre()
                acciones.append(accion)
                iterador = padre
            self.acciones = acciones
            return True

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        # Implmentar aquí lógica agente
        # Estado inicial de la rana
        estado_inicial = Estado(
            percep[entorn_practica1.ClauPercepcio.POSICIO], 0, padre=None
        )
        nombres_ranas = list(estado_inicial.info.keys())
        estado_inicial.generar_hijos(nombres_ranas[0])
        return entorn_practica1.AccionsRana.ESPERAR
