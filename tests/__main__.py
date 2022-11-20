import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(str(BASE_DIR))

from tests import (
    agent_busq_no_informado,
    agent_a_estrella,
    agent_minimax,
    agent_genetico,
)
from tests import joc


def main():
    args = sys.argv[1:]
    if len(args) == 0:
        print(
            "\nUsage: python __main__.py <test_num>\nTests:\n\t1: Busqueda no informada\n\t2: A*\n\t3: Minimax\n\t4: Genetico"
        )
        return

    test_name = args[0]

    if test_name == "1":
        rana = agent_busq_no_informado.RanaBusquedaNoInformada("Miquel")

    if test_name == "2":
        rana = agent_a_estrella.RanaEstrella("Miquel")

    if test_name == "3":
        rana = agent_minimax.RanaMiniMax("Miquel")
        rana2 = agent_minimax.RanaMiniMax("Pep")

    if test_name == "4":
        rana = agent_genetico.RanaGenetica("Miquel")

    if test_name not in ["1", "2", "3", "4"]:
        print("Test not found")
        return

    if test_name == "3":
        lab = joc.Laberint([rana, rana2], parets=True)
    else:
        lab = joc.Laberint([rana], parets=True)

    lab.comencar()


if __name__ == "__main__":
    main()
