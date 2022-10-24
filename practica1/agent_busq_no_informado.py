from agent import Rana


class RanaBusquedaNoInformada(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.abiertos = []
        self.cerrados = []
        self.estado_inicial = None

    def _buscar(self):
        pass