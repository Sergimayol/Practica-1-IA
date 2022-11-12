from agent import Rana
from practica1.agent import Estado
from ia_2022 import entorn
from practica1 import entorn as entorn_practica1


class RanaBusquedaNoInformada(Rana):
    def __init__(self, *args, **kwargs):
        self.__abiertos = None
        self.__cerrados = None
        self.__acciones = None
        self.__turno = 0

    def pinta(self, display):
        pass

    def _buscar(self, estat: Estado):
        #Lista de estados abiertos
        self.__abiertos = []
        #Conjunto de estados cerrados
        self.__cerrados = set()
        #Añadimos el estado inicial a la lista de abiertos
        self.__abiertos.append(estat)
        #Declaramos el estado actual como None
        estado_actual = None
        #Mientras la lista de abiertos no esté vacía
        while len(self.__abiertos) > 0:
            #El estado actual es el primer elemento de la lista de abiertos
            estado_actual = self.__abiertos[0]
            #Los estados abiertos son desde el segundo elemento hasta el final
            self.__abiertos = self.__abiertos[1:]

            #Si el estado actual está en la lista de cerrados, no hacemos nada
            if estado_actual in self.__cerrados:
                continue
            
            #Si el estado actual es válido
            if not estado_actual.es_valid():
                #Añadimos el estado actual a la lista de cerrados
                self.__cerrados.add(estado_actual)
                continue
            
            #Se generan estados hijos del estado actual
            estados_hijos = estado_actual.genera_fills()

            #Si el estado actual es meta salir del bucle
            if estado_actual.es_meta():
                break
            
            #Añadimos los estados hijos a la lista de abiertos
            for estado_hijo in estados_hijos:
                self.__abiertos.append(estado_hijo)

            #Añadimos el estado actual a la lista de cerrados
            self.__cerrados.add(estado_actual)

        #Si el estado actual no existe: ERROR
        if estado_actual is None:
            raise ValueError("Error impossible")

        #Si el estado actual es meta
        if estado_actual.es_meta():
            #Se genera la lista de acciones
            accions = []
            #Copiamos el estado actual en un iterador
            iterador = estado_actual
            
            #Mientras el iterador padre no sea None
            while iterador.padre is not None:

                padre, accio = iterador.padre
                #Añadimos la acción a la lista de acciones
                accions.append(accio)
                #El iterador es el padre
                iterador = padre
            self.__acciones = accions
            return True
        else:
            return False


    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
            # Guardamos las percepciones
            percepciones = percep.to_dict()
            # Guardamos las claves de las percepciones
            clave = list(percepciones.keys())
            # Pasamos al estado el las claves de las percepciones
            estado = Estado(percep[clave[0]],percep[clave[1]], percep[clave[2]])

            #Si no hay acciones
            if self.__acciones is None:
                #Buscamos acciones para el estado
                self._buscar(estado)
            
            #Si hay acciones
            if self.__acciones:
                #Si el turno es mayor que 0
                if(self.__turno > 0):
                    #Restar 1 al turno
                    self.__turno -= 1
                    #La rana ESPERA
                    return entorn_practica1.AccionsRana.ESPERAR
                else: 
                    #La acción es la última de la lista de acciones
                    accion=self.__acciones.pop()
                    #Si la acción es BOTAR
                    if(accion[0] == entorn_practica1.AccionsRana.BOTAR):
                        #Sumar 2 al turno
                        self.__turno=2
                    #Retornar acción y dirección
                    return accion[0], accion[1]
            else:
                return entorn_practica1.AccionsRana.ESPERAR