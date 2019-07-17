import numpy as np
import heapq
import math

from .graph2D import Graph2D


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
    def breadthFirst(start, goal, obj, maze):
        graph = Graph2D(start, goal, obj.actions, maze)
        frontier = [ graph.startNode ]

        try:
            while True:
                node = frontier.pop(0)
                for edge in graph.newEdges(node):             
                    if edge['isGoal']:
                        return graph.makePath(edge)

                    frontier.append(edge)

        except:
            return graph.makePath(None)
            


    """
    Métodos de busca individuais com heurísticas, baseados na minimização de uma função custo.
    """
    # Busca uniforme
    # Não utiliza heurística.
    @staticmethod
    def uniformCost(start, goal, obj, maze):
        cost = lambda node: node['pathCost']
        return Search.leastCost(Graph2D(start, goal, obj.actions, maze), cost)
        

    # Busca A* (A Star).
    # Utiliza a distância de manhattan como heurística.
    # OBS: Baseada em 4 movimentos possíveis.
    @staticmethod
    def AStar(start, goal, obj, maze):
        cost = lambda node: node['pathCost'] + Search.manhattanDistance(goal, node['position'])
        return Search.leastCost(Graph2D(start, goal, obj.actions, maze), cost)


    # Busca greedy
    # Utiliza a distância de manhattan como heurística.
    # OBS: Baseada em 4 movimentos possíveis.
    @staticmethod
    def greedy(start, goal, obj, maze):
        cost = lambda node: Search.manhattanDistance(goal, node['position'])
        return Search.leastCost(Graph2D(start, goal, obj.actions, maze), cost)


    # Busca A* "Direta"
    # Utiliza o produto vetorial como parte da heurística para favorecer
    # caminhos próximos à linha reta que conecta o início ao fim.
    @staticmethod
    def AStarDirect(start, goal, obj, maze):
        vector = (start[0] - goal[0], start[1] - goal[1])
        cost = lambda node: node['pathCost'] + Search.manhattanDistance(goal, node['position']) \
                            + 0.0001*Search.crossDistance((node['position'][0] - goal[0], node['position'][1] - goal[1]), vector)
        return Search.leastCost(Graph2D(start, goal, obj.actions, maze), cost)


    # Função de busca que minimiza uma função custo genérica.
    @staticmethod
    def leastCost(graph, cost):
        # Nó inicial.
        frontier = [ (0, 0, graph.startNode) ]
        i = 0

        try:
            while True:
                # Extrai o nó com menor custo.
                node = heapq.heappop(frontier)[-1]

                # A primeira vez que visita um nó é quando encontra o menor caminho até ele.
                if node['visited']:
                    continue

                # Encontrou o menor caminho.
                if node['isGoal']:
                    return graph.makePath(node)

                # Adiciona novos nós para serem explorados.
                for edge in graph.newEdges(node):
                    i -= 1
                    heapq.heappush(frontier, (cost(edge), i, edge))

        except:
            return graph.makePath(None)



    """
    Heurísticas
    """
    # Distância de Manhattan
    # Considera apenas 4 movimentos possíveis em uma grade.
    @staticmethod
    def manhattanDistance(position1, position2):
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


    # Distância de Chebyshev
    # Considera 8 movimentos possíveis em uma grade.
    @staticmethod
    def chebyshevDistance(position1, position2):
        return max((abs(position1[0] - position2[0]), abs(position1[1] - position2[1])))


    # Distância Euclidiana
    # Calcula o comprimento da linha reta que conecta dois pontos.
    @staticmethod
    def euclideanDistance(position1, position2):
        return ((position1[0] - position2[0])**2 + (position1[1] - position2[1])**2)**0.5


    # Distância "Produto vetorial"
    # Calcula o valor do produto vetorial entre dois vetores
    # Pode ser utilizado para compor heurística com um vetor ligando o ponto atual
    # ao objetivo e outro vetor ligando a origem ao objetivo.
    @staticmethod
    def crossDistance(vector1, vector2):
        return abs(vector1[0]*vector2[1] - vector2[0]*vector1[1])
