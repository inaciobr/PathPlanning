import numpy as np


__all__ = ['getFourMoves', 'makePath']


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
            'action': _actions[node['action']]
        })

        node = node['parent']

    solution.reverse()
    return solution