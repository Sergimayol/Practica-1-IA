import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))

from practica1 import agent_busq_no_informado, agent_a_estrella
from practica1 import agent_minimax
from practica1 import agent, joc
from practica1 import entorn as entorn_practica1


def main():

    # rana = agent_busq_no_informado.RanaBusquedaNoInformada("Miquel")
    rana = agent_minimax.RanaMiniMax("Miquel")
    rana2 = agent_minimax.RanaMiniMax("Pep")
    lab = joc.Laberint([rana, rana2], parets=True)
    lab.comencar()


if __name__ == "__main__":
    main()
