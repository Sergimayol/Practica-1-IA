from agent import Rana, Estado
from ia_2022 import entorn
from practica1 import joc, entorn as entorn_practica1
from practica1.entorn import ClauPercepcio, AccionsRana


class RanaMiniMax(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__abiertos = None
        self.__cerrados = None
        self.__acciones = None

    def pinta(self, display):
        pass

    def busqueda_minimax(self, estado: Estado, turno: bool = True) -> int:
        """Algoritmo de busqueda minimax
        Min -> False
        Args:
            estado_inicial (Estado): Estado inicial del problema
            turno (bool, optional): Turno de la rana. Defaults to True. Min -> False, Max -> True
        Returns:
            int: Valor de la mejor accion
        """
        puntuacion = estado.puntuacion()
        if puntuacion != 0:
            return puntuacion

        puntuacion_hijos = [
            self.busqueda_minimax(hijo, not turno) for hijo in estado.generar_hijos()
        ]

        return max(puntuacion_hijos) if turno else min(puntuacion_hijos)

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:

        estado_inicial = Estado(percep.to_dict(), 0, padre=None)

        if self.__acciones is None:
            self.busqueda_minimax(estado_inicial, True)

        acciones = []
        iterador = estado_inicial

        while iterador.padre() is not None:
            padre, accion = iterador.padre()
            iterador = padre
            acciones.append(accion)

        if self.__acciones:
            acc = self.__acciones.pop()
            return acc[0], acc[1]

        return AccionsRana.ESPERAR
