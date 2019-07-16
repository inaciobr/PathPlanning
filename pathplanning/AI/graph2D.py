import numpy as np

"""
Implementação de do grafo 2D utilizado nos algoritmos de busca.
"""
class Graph2D:
    def __init__(self, start, goal, obj, maze, cost = None, initialCost = 0):
        self.node = {}
        self.cost = cost

        self.obj = obj
        self.actions = obj.actions
        self.maze = maze
        self.neighbors = maze.getNeighbors

        self.startNode = self.addNode(start, None, initialCost, 'S')
        self.goalNode = self.addNode(goal, None, np.inf, ' ', state = 'G')


    # Adiciona um novo nó ao grafo.
    def addNode(self, pos, parent, pathCost, action, state = 'U'):
        self.node[pos] = {
            'state': state, 
            'position': pos,
            'pathCost': pathCost,
            'action': action,
            'parent': parent
        }

        return self.node[pos]


    # Retorna as arestas ainda não visitadas de um nó.
    def newEdges(self, node):
        for neighbor in self.neighbors(node['position'], self.actions, node['pathCost']):
            eNode = self.node.get(neighbor['position'])

            if eNode is None:
                yield self.addNode(neighbor['position'], node, neighbor['pathCost'], neighbor['action'])

            elif eNode['state'] != 'V' and neighbor['pathCost'] < eNode['pathCost']:
                eNode['pathCost'] = neighbor['pathCost']
                eNode['action'] = neighbor['action']
                eNode['parent'] = node
                yield eNode


    # Monta o caminho encontrado.
    def makePath(self, node):
        solution = [ ]

        if node is None:
            return solution

        while node['parent'] is not None:
            solution.append({'position': node['position'],
                             'pathCost': node['pathCost'],
                             'action': node['action']})
            node = node['parent']

        solution.reverse()
        return solution
