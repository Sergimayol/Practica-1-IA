"""

ClauPercepcio:
    POSICIO = 0
    OLOR = 1
    PARETS = 2
"""
from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import ClauPercepcio, AccionsRana, Direccio


class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)

    def pinta(self, display):
        pass

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass


class Estado:
    def __init__(self, info: dict = None, peso: int = 0, padre=None):
        self.__info = info
        self.__peso = peso
        self.__padre = padre

    def __hash__(self) -> int:
        return hash(tuple(self.__info))

    @property
    def info(self):
        return self.__info

    def padre(self):
        return self.__padre

    def __str__(self) -> str:
        return str(self.__info)

    def __eq__(self, other):
        return self.__info == other.info

    @property
    def pare(self):
        return self.__pare

    @pare.setter
    def pare(self, value):
        self.__pare = value

    def es_legal(self) -> bool:
        # TODO: implementar
        pass

    def es_meta(self) -> bool:
        # TODO: implementar
        return False

    def generar_hijos(self) -> list:
        # TODO: implementar

        pass
