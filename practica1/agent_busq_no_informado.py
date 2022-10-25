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

            if not actual.es_segur():
                self.cerrados.add(actual)
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
        estado_inicial = Estado(percep[entorn_practica1.ClauPercepcio.POSICIO], 0, padre=None)
        if self.acciones is None:
            self._buscar(estado = estado_inicial)
        if len(self.acciones) > 0:
            return entorn_practica1.AccionsRana.MOURE, self.acciones.pop()
        
        else:
            # EN un futuro cambiar, de momento es para que no de error
            return entorn_practica1.AccionsRana.ESPERAR
