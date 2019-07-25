"""
Algoritmos de busca para encontrar o caminho que minimiza um determiando custo
entre dois pontos, sem conhecimento sobre detalhes do ambiente.
"""
from collections import deque
from .graph2D import Graph2D


__all__ = ['breadthFirst']


# Busca em largura.
# Todos as expansões são consideradas com custo 1.
def breadthFirst(start, goal, mask, actions):
    nodes = {
        start: {
            'position': start,
            'pathCost': 0,
            'action': 'S',
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
                            return Graph2D.makePath(nodes[edge])

                        frontier.append(nodes[edge])
                except:
                    pass
    except:
        return Graph2D.makePath(None)
