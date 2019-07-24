from collections import deque, namedtuple
import numpy as np
import heapq

from .graph2D import Graph2D
from .heuristic import Heuristic


"""
Algoritmos de busca para encontrar o caminho que minimiza um determiando custo entre dois pontos.
"""
class Search:
    """
    Métodos simples de busca.
    """
    # Busca em largura.
    # Todos as expansões são consideradas com custo 1.
    @staticmethod
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


    # Função de busca que minimiza uma função custo genérica.
    @staticmethod
    def leastCost(start, goal, graph, cost):
        # Nó inicial.
        openList = [ (0, 0, graph.addNode(start, 0, 'S')) ]
        i = 0

        while len(openList):
            # Extrai o nó com menor custo.
            _, _, node = heapq.heappop(openList)

            # A primeira vez que visita um nó é quando encontra o menor caminho até ele.
            if node['visited']:
                continue

            # Encontrou o menor caminho.
            if node['position'] == goal:
                return graph.makePath(node)

            # Adiciona novos nós para serem explorados.
            for edge in graph.newEdges(node):
                i -= 1
                heapq.heappush(openList, (cost(edge), i, edge))

        return graph.makePath(None)



    """
    Métodos de busca individuais com heurísticas, baseados na minimização de uma função custo.
    """
    # Busca A* (A Star).
    # Utiliza a distância de manhattan como heurística.
    # OBS: Baseada em 4 movimentos possíveis.
    @staticmethod
    def AStar(start, goal, field, actions):
        cost = lambda node: node['pathCost'] + Heuristic.manhattanDistance(goal, node['position'])
        return Search.leastCost(start, goal, Graph2D(field, actions), cost)


    # Busca uniforme
    # Não utiliza heurística.
    @staticmethod
    def uniformCost(start, goal, field, actions):
        cost = lambda node: node['pathCost']
        return Search.leastCost(start, goal, Graph2D(field, actions), cost)
        

    # Busca greedy
    # Utiliza a distância de manhattan como heurística.
    # OBS: Baseada em 4 movimentos possíveis.
    @staticmethod
    def greedy(start, goal, field, actions):
        cost = lambda node: Heuristic.manhattanDistance(goal, node['position'])
        return Search.leastCost(start, goal, Graph2D(field, actions), cost)


    # Busca A* "Direta"
    # Utiliza o produto vetorial como parte da heurística para favorecer
    # caminhos próximos à linha reta que conecta o início ao fim.
    @staticmethod
    def AStarDirect(start, goal, field, actions):
        vector = (start[0] - goal[0], start[1] - goal[1])
        cost = lambda node: node['pathCost'] + Heuristic.manhattanDistance(goal, node['position']) \
                            + 0.0001*Heuristic.crossDistance((node['position'][0] - goal[0], node['position'][1] - goal[1]), vector)

        return Search.leastCost(start, goal, Graph2D(field, actions), cost)
