from . import straight
from . import path

from .include import geneticAlgorithm


__all__ = ['geneticSearch']


def cost(start, goal, position):
    return 1


def geneticSearch(start, goal, field, actions):
    # Tentativa 0 (Linha reta)
    if straight.checkStraightLine(start, goal, field.mask):
        return straight.straightLine(start, goal, field, actions)

    # Obtém máscara de posições possíveis
    mask = field.mask.copy()
    mask[start] = False
    mask[goal] = False

    # Obtém lista de posições válidas
    # Posição inicial estará sempre no índice 0
    # Posição final estará sempre no índice -1
    validPositions = list(zip(*mask.nonzero()))
    validPositions.append(goal)
    validPositions.insert(0, start)
    
    # Tentativa 1 (1 ponto intermediário)
    

    return path.makePath(None)
