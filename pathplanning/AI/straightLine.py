"""
Algoritmos baseados em linhas retas
"""
import numba as nb

from .heuristic import Heuristic


__all__ = ['checkStraightLine', 'straightLine']


# Verifica se existe a linha reta que liga dois pontos.
@nb.njit(nb.boolean(nb.types.UniTuple(nb.int64, 2), nb.types.UniTuple(nb.int64, 2), nb.boolean[:, :]))
def checkStraightLine(start, goal, mask):
    px, py = start

    vecX = goal[0] - px
    vecY = goal[1] - py

    dirX = 1 if vecX > 0 else -1
    dirY = 1 if vecY > 0 else -1

    stepX = dirX * vecX
    stepY = dirY * vecY

    i = 0.5*stepY
    j = 0.5*stepX

    cross = stepY * (stepX + 0.5) + stepX * (stepY + 0.5)

    while mask[px, py] and i + j < cross:
        if i < j:
            px += dirX
            i += stepY
        else:
            py += dirY
            j += stepX

    return mask[px, py]


# Algoritmo que visa puramente seguir uma linha reta.
# Se não for possível seguir o caminho direto, ele retorna o caminho até o obstáculo
# que interceptou o movimento.
@staticmethod
def straightLine(start, goal, field, actions):
    vector = (start[0] - goal[0], start[1] - goal[1])
    cost = lambda node: Heuristic.crossDistance((node[0] - goal[0], node[1] - goal[1]), vector)

    node = start
    pathCost = 0

    # Utiliza apenas as ações que apontam na direção do objetivo.
    gActions = [ act for act in actions if vector[0]*act['direction'][0] <= 0 and vector[1]*act['direction'][1] <= 0 ]

    path = [{
        'position': node,
        'pathCost': pathCost,
        'action': 'S'
    }]

    while node != goal:
        edgePos = [ (node[0] + act['direction'][0], node[1] + act['direction'][1]) for act in gActions ]
        _, node, act = min(zip(map(cost, edgePos), edgePos, gActions))

        if not field.mask[node]:
            break

        pathCost += act['cost']

        path.append({
            'position': node,
            'pathCost': pathCost,
            'action': act['action']
        })

    return path
