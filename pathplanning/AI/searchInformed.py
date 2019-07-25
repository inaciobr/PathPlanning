"""
Algoritmos de busca para encontrar o caminho que minimiza um determiando custo
entre dois pontos com o uso de informações sobre o mapa.
"""
import heapq

from .graph2D import Graph2D
from . import heuristic


__all__ = ['AStar', 'uniformCost', 'greedy', 'AStarDirect', 'leastCost']


# Busca A* (A Star).
# Utiliza a distância de manhattan como heurística.
# OBS: Baseada em 4 movimentos possíveis.
def AStar(start, goal, field, actions):
    cost = lambda node: node['pathCost'] + heuristic.manhattanDistance(goal, node['position'])
    return leastCost(start, goal, field, actions, cost)


# Busca uniforme
# Não utiliza heurística.
def uniformCost(start, goal, field, actions):
    cost = lambda node: node['pathCost']
    return leastCost(start, goal, field, actions, cost)
    

# Busca greedy
# Utiliza a distância de manhattan como heurística.
# OBS: Baseada em 4 movimentos possíveis.
def greedy(start, goal, field, actions):
    cost = lambda node: heuristic.manhattanDistance(goal, node['position'])
    return leastCost(start, goal, field, actions, cost)


# Busca A* "Direta"
# Utiliza o produto vetorial como parte da heurística para favorecer
# caminhos próximos à linha reta que conecta o início ao fim.
def AStarDirect(start, goal, field, actions):
    vector = (start[0] - goal[0], start[1] - goal[1])
    cost = lambda node: (
        node['pathCost'] + heuristic.manhattanDistance(goal, node['position'])
        + 0.0001*heuristic.crossDistance((node['position'][0] - goal[0], node['position'][1] - goal[1]), vector)
    )

    return leastCost(start, goal, field, actions, cost)


# Função de busca que minimiza uma função custo genérica.
def leastCost(start, goal, field, actions, cost):
    mask = field.mask

    closedList = { }
    openList = [ (0, 0, { 'position': start, 'pathCost': 0, 'action': 'S', 'parent': None }) ]

    i = 0
    try:
        while True:
            _, _, node = heapq.heappop(openList)

            if node['position'] in closedList:
                continue

            closedList[node['position']] = node

            if node['position'] == goal:
                return Graph2D.makePath(node)

            posX, posY = node['position']
            for action in actions:
                dx, dy = action['direction']
                edge = (posX + dx, posY + dy)
                try:
                    if edge not in closedList and mask[edge] and 0 <= edge[0] and 0 <= edge[1]:
                        edgeNode = {
                            'position': edge,
                            'pathCost': node['pathCost'] + action['cost'],
                            'action': action['action'],
                            'parent': node
                        }

                        i -= 1
                        heapq.heappush(openList, (cost(edgeNode), i, edgeNode))
                except:
                    pass

    except:
        return Graph2D.makePath(None)
