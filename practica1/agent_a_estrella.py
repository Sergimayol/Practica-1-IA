from queue import PriorityQueue
from agent import Rana
from practica1.agent import Estado
from ia_2022 import entorn
from practica1 import entorn as entorn_practica1
from practica1.entorn import ClauPercepcio, AccionsRana, Direccio
import copy
class Estado:
    def __init__(self, info: dict, coste: int, padre=None):
        self.__info = info  # información sobre la rana
        self.__padre = padre  # padre del estado
        self.__coste = coste  # coste del estado
        self.__max_tablero = 7

    def __hash__(self) -> int:
        return hash(tuple(self.__info))

    @property
    def info(self):
        return self.__info

    def es_meta(self, nombre_rana: str) -> bool:
        return self.__info.get(ClauPercepcio.POSICIO).get(
            nombre_rana
        ) == self.__info.get(ClauPercepcio.OLOR)
    def get_posicion(self):
        return self.__info.get(ClauPercepcio.POSICIO).get('Miquel')

    def get_comida(self):
        return self.__info.get(ClauPercepcio.OLOR)
    @property
    def padre(self):
        return self.__padre

    @padre.setter
    def padre(self, value):
        self.__padre = value

    def __getitem__(self, key):
        if key == 0:
            return self.__info.get(ClauPercepcio.POSICIO)
        elif key == 1:
            return self.__info.get(ClauPercepcio.OLOR)
        elif key == 2:
            return self.__info.get(ClauPercepcio.PARETS)

    def __setitem__(self, key, value):
        self.__info[key] = value

    def __str__(self) -> str:
        return str(self.__info)

    def __eq__(self, __o: object) -> bool:
        return self.__info.get(ClauPercepcio.POSICIO) == __o.info.get(
            ClauPercepcio.POSICIO
        )
    def __lt__(self, other):
        return False

    def calcular_heuritica(self, nombre_rana) -> int:
        # obtener la posicion de la rana
        pos_rana = self.__info.get(ClauPercepcio.POSICIO).get(nombre_rana)
        # obtener la posicion del olor
        pos_olor = self.__info.get(ClauPercepcio.OLOR)
        # calcular la distancia de Manhattan
        return abs(pos_rana[0] - pos_olor[0]) + abs(pos_rana[1] - pos_olor[1])

    def get_frog_names(self) -> list[str]:
        return list(self.__info.get(ClauPercepcio.POSICIO).keys())

    def legal(self, pos_actual: tuple) -> bool:
        # obtener los muros
        walls = self.__info.get(ClauPercepcio.PARETS)
        # comprobar si la posicion actual esta en los muros
        return pos_actual not in walls

    def generar_hijos(self, nombre_rana: str) -> list:
        """
        Esta funcion genera los posibles estados hijos de un estado,
        siempre y cuando sean legales.

        Args:
            nombre_rana (_str_): nombre de la rana que se desea generar los hijos

        Returns:
            _list_: list de estados hijos generados
        """
        debug, print_hijos = False, True

        hijos = []

        # pos 0 = x, pos 1 = y (empiezan en 0)
        pos_actual = self.__info.get(ClauPercepcio.POSICIO).get(nombre_rana)
        print("Posición padre:", pos_actual)
        if pos_actual[0] > 0:
            # movimientos a la izquierda
            new_pos = (pos_actual[0] - 1, pos_actual[1])
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(Estado(hijo, self.__coste + 1, self))

            if debug:
                print("movimiento a la izquierda +1")
                print("hijo: ", hijo)
            if pos_actual[0] > 1:
                new_pos = (pos_actual[0] - 2, pos_actual[1])
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(Estado(hijo, self.__coste + 2, self))
                if debug:
                    print("movimiento a la izquierda +2")
                    print("hijo: ", hijo)

        if pos_actual[0] < self.__max_tablero:
            # movimientos a la derecha
            new_pos = (pos_actual[0] + 1, pos_actual[1])
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(Estado(hijo, self.__coste + 1, self))

            if debug:
                print("movimiento a la derecha +1")
                print("hijo: ", hijo)

            if pos_actual[0] < self.__max_tablero - 1:
                new_pos = (pos_actual[0] + 2, pos_actual[1])
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(Estado(hijo, self.__coste + 2, self))
                if debug:
                    print("movimiento a la derecha +2")
                    print("hijo: ", hijo)

        if pos_actual[1] > 0:
            # movimientos hacia arriba
            new_pos = (pos_actual[0], pos_actual[1] - 1)
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(Estado(hijo, self.__coste + 1, self))

            if debug:
                print("movimiento hacia arriba +1")
                print("hijo: ", hijo)
            if pos_actual[1] > 1:
                new_pos = (pos_actual[0], pos_actual[1] - 2)
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(Estado(hijo, self.__coste + 2, self))
                if debug:
                    print("movimiento hacia arriba +2")
                    print("hijo: ", hijo)

        if pos_actual[1] < self.__max_tablero:
            # movimientos hacia abajo
            new_pos = (pos_actual[0], pos_actual[1] + 1)
            if self.legal(new_pos):
                hijo = copy.deepcopy(self.__info)
                hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                hijos.append(Estado(hijo, self.__coste + 1, self))

            if debug:
                print("movimiento hacia abajo +1")
                print("hijo: ", hijo)
            if pos_actual[1] < self.__max_tablero - 1:
                new_pos = (pos_actual[0], pos_actual[1] + 2)
                if self.legal(new_pos):
                    hijo = copy.deepcopy(self.__info)
                    hijo[ClauPercepcio.POSICIO][nombre_rana] = new_pos
                    hijos.append(Estado(hijo, self.__coste + 2, self))

                if debug:
                    print("movimiento hacia abajo +2")
                    print("hijo: ", hijo)

        if print_hijos:
            for hijo in hijos:
                print("hijo: ", hijo.info.get(ClauPercepcio.POSICIO))

        return hijos

class RanaEstrella(Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__abiertos = None
        self.__cerrados = None
        self.__acciones = None
        self.__torn = 0

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
                print("Estado hijo", estado_hijo)
                self.__abiertos.put((estado_hijo.calcular_heuritica("Miquel"), estado_hijo))

            self.__cerrados.add(estado_actual)
            print("Estado actual: ", estado_actual)
            
            if estado_actual.es_meta("Miquel"):
                acciones = []
                iterador = estado_actual
                while iterador.padre is not None:
                    
                    accion = iterador.padre
                    print("Accion", str(accion))
                    acciones.append(accion[0].get("Miquel"))
                    iterador = iterador.padre

            # acciones.append(iterador.padre[0].get("Miquel"))
                self.__acciones = acciones
            return True
        else:
            return False               

    def actua(
        self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        estado_inicial = Estado(percep.to_dict(), 0, padre=None)
        
        if self.__acciones is None:
            self._buscar(estado_inicial)
            estado_pizza = estado_inicial.get_comida()
            print("Estado pizza: ", estado_pizza)
            #self.__acciones.insert(0, estado_pizza)
            print("Acciones: ", self.__acciones)


        if self.__acciones:
            if(self.__torn>0):
                self.__torn-=1
                print("Espera un turno")
                return AccionsRana.ESPERAR
            else:
                posicion_rana = estado_inicial.get_posicion()
                print("Estado:", posicion_rana)
                siguiente_posicion=self.__acciones.pop()
                print("Siguiente estado:"+str(siguiente_posicion))
                resultado = 0
                resultado = abs(posicion_rana[0] - siguiente_posicion[0]) + abs(posicion_rana[1] - siguiente_posicion[1])
                print("Resultado: ",resultado)
                if (self.__torn == 0 and resultado == 1):
                    if posicion_rana[0] < siguiente_posicion[0]:
                        self.__torn += 1
                        return AccionsRana.MOURE, Direccio.DRETA
                    elif posicion_rana[0] > siguiente_posicion[0]:
                        self.__torn += 1
                        return AccionsRana.MOURE, Direccio.ESQUERRE
                    elif posicion_rana[1] < siguiente_posicion[1]:
                        self.__torn += 1
                        return AccionsRana.MOURE, Direccio.BAIX
                    elif posicion_rana[1] > siguiente_posicion[1]:
                        self.__torn += 1
                        return AccionsRana.MOURE, Direccio.DALT
                    #retornam acció i direcció
                    else: 
                        return AccionsRana.ESPERAR
                elif (self.__torn == 0 and resultado > 1):
                    if posicion_rana[0] < siguiente_posicion[0]:
                        self.__torn += 2
                        return AccionsRana.BOTAR, Direccio.DRETA          
                    elif posicion_rana[0] > siguiente_posicion[0]:
                        self.__torn += 2
                        return AccionsRana.BOTAR, Direccio.ESQUERRE
                    elif posicion_rana[1] < siguiente_posicion[1]:
                        self.__torn += 2
                        return AccionsRana.BOTAR, Direccio.BAIX
                    
                    elif posicion_rana[1] > siguiente_posicion[1]:
                        self.__torn += 2
                        return AccionsRana.BOTAR, Direccio.DALT
                    #retornam acció i direcció
                else:
                    return AccionsRana.ESPERAR
            
        
