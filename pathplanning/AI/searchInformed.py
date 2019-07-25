"""
Algoritmos de busca para encontrar o caminho que minimiza um determiando custo
entre dois pontos com o uso de informações sobre o mapa.
"""
import heapq

from .graph2D import Graph2D
from .heuristic import Heuristic


__all__ = ['AStar', 'uniformCost', 'greedy', 'AStarDirect', 'leastCost']


# Busca A* (A Star).
# Utiliza a distância de manhattan como heurística.
# OBS: Baseada em 4 movimentos possíveis.
def AStar(start, goal, field, actions):
    cost = lambda node: node['pathCost'] + Heuristic.manhattanDistance(goal, node['position'])
    return leastCost(start, goal, Graph2D(field, actions), cost)


# Busca uniforme
# Não utiliza heurística.
def uniformCost(start, goal, field, actions):
    cost = lambda node: node['pathCost']
    return leastCost(start, goal, Graph2D(field, actions), cost)
    

# Busca greedy
# Utiliza a distância de manhattan como heurística.
# OBS: Baseada em 4 movimentos possíveis.
def greedy(start, goal, field, actions):
    cost = lambda node: Heuristic.manhattanDistance(goal, node['position'])
    return leastCost(start, goal, Graph2D(field, actions), cost)


# Busca A* "Direta"
# Utiliza o produto vetorial como parte da heurística para favorecer
# caminhos próximos à linha reta que conecta o início ao fim.
def AStarDirect(start, goal, field, actions):
    vector = (start[0] - goal[0], start[1] - goal[1])
    cost = lambda node: node['pathCost'] + Heuristic.manhattanDistance(goal, node['position']) \
                        + 0.0001*Heuristic.crossDistance((node['position'][0] - goal[0], node['position'][1] - goal[1]), vector)

    return leastCost(start, goal, Graph2D(field, actions), cost)


# Função de busca que minimiza uma função custo genérica.
def leastCost(start, goal, graph, cost):
    openList = [ (0, 0, graph.addNode(start, 0, 'S')) ]
    i = 0

    while len(openList):
        # Extrai o nó com menor custo.
        _, _, node = heapq.heappop(openList)

        if node['visited']:
            continue

        if node['position'] == goal:
            return graph.makePath(node)

        # Adiciona novos nós para serem explorados.
        for edge in graph.newEdges(node):
            i -= 1
            heapq.heappush(openList, (cost(edge), i, edge))

    return graph.makePath(None)
