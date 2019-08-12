from . import searchInformed

import numpy as np


__all__ = ['getFourMoves', 'makePath', 'printGraphStates', 'connectPoints']


_actions = {
    0x00: {'action': 'o'},
    0x01: {'action': '↑'},
    0x02: {'action': '↓'},
    0x04: {'action': '←'},
    0x08: {'action': '→'},

    0x05: {'action': '↖'},
    0x06: {'action': '↙'},
    0x09: {'action': '↗'},
    0x0A: {'action': '↘'},
}


def getFourMoves():
    return [
        { 'action': 0x01, 'cost': 1.0, 'direction': (-1,  0) },
        { 'action': 0x02, 'cost': 1.0, 'direction': (+1,  0) },
        { 'action': 0x04, 'cost': 1.0, 'direction': ( 0, -1) },
        { 'action': 0x08, 'cost': 1.0, 'direction': ( 0, +1) }
    ]


# Monta o caminho encontrado.
def makePath(node):
    solution = [ ]

    while node is not None:
        solution.append({
            'position': node['position'],
            'pathCost': node['pathCost'],
            'action': _actions[node['action']]['action']
        })

        node = node['parent']

    solution.reverse()
    return solution


# Retorna um caminho composto pela união de diversos pontos
def connectPoints(start, goal, field, actions, points):
    path = [ ]

    points = list(zip(*points))
    points.insert(0, start)
    points.append(goal)

    for i in range(len(points) - 1):
        path.extend(searchInformed.AStarDirect(points[i], points[i + 1], field, actions))

    return path


def printGraphStates(nodes, field):
    # Identificação das colunas
    mapa = '     ' \
         + ' '.join("{:03}".format(i) for i in range(field.shape[1])) \
         + '\n'

    for i, line in enumerate(field):
        mapa += "{:03} ".format(i)

        for j, _ in enumerate(line):
            mapa += "| " + (
                'V' if (i, j) in nodes else
                ' '
            ) + " "

        mapa += '\n'

    print(mapa)
