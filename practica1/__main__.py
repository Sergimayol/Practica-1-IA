import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))

from practica1 import agent_busq_no_informado
from practica1 import agent, joc
from practica1 import entorn as entorn_practica1


def main():
    rana = agent_busq_no_informado.Rana("Miquel")
    lab = joc.Laberint([rana], parets=True)
    pos_rana = rana.get_rana()
    pizza = lab.get_pizza()
    print(pizza)    # Posición estado inicial pizza
    print(pos_rana) # Posición estado inicial rana
    lab.comencar()



if __name__ == "__main__":
    main()
