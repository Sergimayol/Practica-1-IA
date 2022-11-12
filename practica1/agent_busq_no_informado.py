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
        self.__abiertos = []
        self.__cerrados = set()

        self.__abiertos.append(estado)
        estado_actual: Estado = None
        profundidad_actual = profundidad
        while len(self.__abiertos) > 0 and profundidad_actual >= 0:
            estado_actual = self.__abiertos.pop()
            if estado_actual in self.__cerrados:
                continue

            if estado_actual.es_meta("Miquel"):
                break

            # Cambiar el nombre rana dinámico
            estados_hijos = estado_actual.generar_hijos("Miquel")

            for estado_hijo in estados_hijos:
                self.__abiertos.append(estado_hijo)

            self.__cerrados.add(estado_actual)
            profundidad_actual -= 1

        if estado_actual is None:
            raise ValueError("Error imposible")

        if estado_actual.es_meta("Miquel"):
            acciones = []
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
