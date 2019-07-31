"""
Algoritmos de busca para encontrar o caminho que minimiza um determiando custo
entre dois pontos, sem conhecimento sobre detalhes do ambiente.
"""
import numpy as np
from collections import deque

from . import path


__all__ = ['breadthFirst', 'depthFirst', 'iterativeDeepening']


# Busca em largura.
# Todos as expansões são consideradas com custo 1.
def breadthFirst(start, goal, field, actions):
    mask = field.mask
    nodes = {
        start: {
            'position': start,
            'pathCost': 0.0,
            'action': 0x00,
            'parent': None
        }
    }

    frontier = deque([ nodes[start] ])
    try:
        while True:
            node = frontier.popleft()
            posX, posY = node['position']

            for action in actions:
                dx, dy = action['direction']
                edge = (posX + dx, posY + dy)

                try:
                    if edge not in nodes and mask[edge] and 0 <= edge[0] and 0 <= edge[1]:
                        nodes[edge] = {
                            'position': edge,
                            'pathCost': node['pathCost'] + action['cost'],
                            'action': action['action'],
                            'parent': node
                        }
                        
                        if edge == goal:
                            return path.makePath(nodes[edge])

                        frontier.append(nodes[edge])
                except:
                    pass
    except:
        return path.makePath(None)


# Busca em profundidade.
# Todos as expansões são consideradas com custo 1.
# Solução não é, necessariamente, a solução ótima.
def depthFirst(start, goal, field, actions, limit = np.inf):
    mask = field.mask
    node = {
        'position': start,
        'pathCost': 0.0,
        'action': 0x00,
        'parent': None
    }

    nodes = { }
    frontier = deque([ node ])
    try:
        while True:
            node = frontier[-1]

            if node['position'] in nodes or limit < node['pathCost']:
                nodes.pop(node['position'], None)
                frontier.pop()
                continue
            
            nodes[node['position']] = node

            if node['position'] == goal:
                return path.makePath(node)

            posX, posY = node['position']
            for action in actions:
                dx, dy = action['direction']
                edge = (posX + dx, posY + dy)

                try:
                    if edge not in nodes and mask[edge] and 0 <= edge[0] and 0 <= edge[1]:
                        neighbor = {
                            'position': edge,
                            'pathCost': node['pathCost'] + action['cost'],
                            'action': action['action'],
                            'parent': node
                        }

                        frontier.append(neighbor)
                except:
                    pass
    except:
        return path.makePath(None)


def iterativeDeepening(start, goal, field, actions, depth = 0, max = np.inf):
    while depth < max:
        solution = depthFirst(start, goal, field, actions, limit = depth)

        if len(solution):
            return solution

        depth += 1
    
    return path.makePath(None)
