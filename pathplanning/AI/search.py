import numpy as np
import math
import heapq

from .graph2D import Graph2D

"""
Métodos de busca individuais com heurísticas, baseados na minimização de uma função custo.
"""
# Função de busca que minimiza uma função custo genérica.
def leastCost(graph):
    # Nó inicial.
    frontier = [ (0, 0, graph.startNode) ]

    i = 0
    while len(frontier):
        # Extrai o nó com menor custo.
        node = heapq.heappop(frontier)[-1]

        # A primeira vez que visitou um nó é quando encontra o menor caminho até ele.
        if node['state'] == 'V':
            continue

        # Encontrou o menor caminho.
        if node['state'] == 'G':
            return graph.makePath(node)

        # Altera o estado do nó para visitado.
        node['state'] = 'V'

        # Adiciona novos nós para serem explorados.
        for edge in graph.newEdges(node):
            i -= 1
            heapq.heappush(frontier, (graph.cost(edge), i, edge))

    return graph.makePath(None)


def manhattanDistance(position1, position2):
    return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


def AStar(start, goal, obj, maze):
    cost = lambda node: node['pathCost'] + manhattanDistance(goal, node['position'])
    return leastCost(Graph2D(start, goal, obj, maze, cost))

