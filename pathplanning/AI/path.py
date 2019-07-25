import numpy as np

def getFourMoves():
    return [
        { 'action': '^', 'cost': 1, 'direction': (-1,  0), 'hash': 0x01 },
        { 'action': 'v', 'cost': 1, 'direction': (+1,  0), 'hash': 0x02 },
        { 'action': '<', 'cost': 1, 'direction': ( 0, -1), 'hash': 0x04 },
        { 'action': '>', 'cost': 1, 'direction': ( 0, +1), 'hash': 0x08 }
    ]

# Monta o caminho encontrado.
def makePath(node):
    solution = [ ]

    while node is not None:
        solution.append({
            'position': node['position'],
            'pathCost': node['pathCost'],
            'action': node['action']
        })

        node = node['parent']

    solution.reverse()
    return solution
