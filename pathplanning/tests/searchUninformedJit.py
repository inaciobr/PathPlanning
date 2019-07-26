"""
Algoritmos de busca para encontrar o caminho que minimiza um determiando custo
entre dois pontos, sem conhecimento sobre detalhes do ambiente.
"""
from collections import deque
import numba as nb

from . import path



__all__ = ['breadthFirst']


# Busca em largura.
# Todos as expansões são consideradas com custo 1.
@nb.jit
def breadthFirst(start, goal, mask, actions):
    limX, limY = mask.shape

    nodes = {
        start: {
            'position': start,
            'pathCost': 0,
            'action': 'S',
            'parent': None
        }
    }

    frontier = deque([ nodes[start] ])
    while len(frontier):
        node = frontier.popleft()
        posX, posY = node['position']

        for action in actions:
            dx, dy = action['direction']
            edge = (posX + dx, posY + dy)

            if edge not in nodes and 0 <= edge[0] < limX and 0 <= limY and mask[edge]:
                nodes[edge] = {
                    'position': edge,
                    'pathCost': node['pathCost'] + action['cost'],
                    'action': action['action'],
                    'parent': node
                }
                
                if edge == goal:
                    return path.makePath(nodes[edge])

                frontier.append(nodes[edge])

    return path.makePath(None)
