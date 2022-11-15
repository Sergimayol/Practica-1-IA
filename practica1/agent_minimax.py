from agent import Rana
from ia_2022 import entorn
from practica1 import joc, entorn as entorn_practica1
from practica1.entorn import ClauPercepcio, AccionsRana


class Estado:
    pass


class RanaMiniMax(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)

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
        pass

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass
