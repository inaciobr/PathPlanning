"""
Algoritmos baseados em linhas retas
"""
import numba as nb
import numpy as np

from . import cost


__all__ = ['checkStraightLine', 'straightLine', 'straightLinePositions', 'straightLineWeight']


# Algoritmo que visa puramente seguir uma linha reta.
# Se não for possível seguir o caminho direto, ele retorna o caminho até o obstáculo
# que interceptou o movimento.
def straightLine(start, goal, field, actions):
    mask = field.mask
    node = start

    vector = (goal[0] - start[0], goal[1] - start[1])
    distance = lambda n: cost.crossDistance((n[0] - start[0], n[1] - start[1]), vector)

    # Utiliza apenas as ações que apontam na direção do objetivo.
    gActions = [
        act for act in actions
        if 0 <= vector[0]*act['direction'][0] and 0 <= vector[1]*act['direction'][1]
    ]

    path = [{
        'position': node,
        'pathCost': 0,
        'action': 0x00
    }]

    while node != goal:
        edgePos = [
            (node[0] + act['direction'][0], node[1] + act['direction'][1])
            for act in gActions
        ]
        _, node, act = min(zip(map(distance, edgePos), edgePos, gActions))

        if not mask[node]:
            break

        path.append({
            'position': node,
            'pathCost': path[-1]['pathCost'] + act['cost'],
            'action': act['action']
        })

    return path


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


# Verifica se existe a linha reta que liga dois pontos.
@nb.njit(nb.types.UniTuple(nb.int64[:], 2)(nb.types.UniTuple(nb.int64, 2),
                                           nb.types.UniTuple(nb.int64, 2)))
def straightLinePositions(start, goal):
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
    x = [ px ]
    y = [ py ]

    while i + j < cross:
        if i < j:
            px += dirX
            i += stepY
        else:
            py += dirY
            j += stepX

        x.append(px)
        y.append(py)

    return (np.array(x), np.array(y))


# Verifica se existe a linha reta que liga dois pontos.
@nb.njit(nb.int64(nb.types.UniTuple(nb.int64, 2),
                  nb.types.UniTuple(nb.int64, 2),
                  nb.int64[:, :]))
def straightLineWeight(start, goal, weights):
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
    weight = 0

    while i + j < cross:
        if i < j:
            px += dirX
            i += stepY
        else:
            py += dirY
            j += stepX

        weight += weights[px, py]

    return weight
