import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))

from practica1 import (
    agent_busq_no_informado,
    agent_a_estrella,
    agent_minimax,
    agent_genetico,
)
from practica1 import joc


def main():
    # rana = agent_busq_no_informado.RanaBusquedaNoInformada("Miquel")
    # rana = agent_a_estrella.RanaEstrella("Miquel")
    # rana = agent_minimax.RanaMiniMax("Miquel")
    rana = agent_genetico.RanaGenetica("Miquel")
    lab = joc.Laberint([rana], parets=True)
    lab.comencar()


if __name__ == "__main__":
    main()
