import numpy as np

"""
Implementação de do grafo 2D utilizado nos algoritmos de busca.
"""
class Graph2D:
    def __init__(self, start, goal, actions, field, initialCost = 0):
        self.node = {}

        self.actions = actions
        self.field = field

        self.startNode = self.addNode(start, None, initialCost, 'S')
        self.goalNode = self.addNode(goal, None, np.inf, 'G', goal = True)


    # Adiciona um novo nó ao grafo.
    def addNode(self, position, parent, pathCost, action, goal = False):
        self.node[position] = {
            'visited': False,
            'position': position,
            'pathCost': pathCost,
            'action': action,
            'parent': parent,
            'isGoal': goal,
        }

        return self.node[position]


    # Atualiza as informações de um nó.
    def updateNode(self, node, parent, pathCost, action):
        node['parent'] = parent
        node['pathCost'] = pathCost
        node['action'] = action

        return node


    # Retorna as arestas ainda não visitadas de um nó.
    def newEdges(self, node):
        node['visited'] = True
        
        for action in self.actions:
            edgePosition = (node['position'][0] + action['direction'][0], node['position'][1] + action['direction'][1])

            try:
                if not self.field.mask[edgePosition] or edgePosition[0] < 0 or edgePosition[1] < 0:
                    continue
            except:
                continue

            if edgePosition in self.node:
                edgeNode = self.node[edgePosition]

                if not edgeNode['visited'] and node['pathCost'] + action['cost'] < edgeNode['pathCost']:
                    yield self.updateNode(edgeNode, node, node['pathCost'] + action['cost'], action['action'])
            else:
                yield self.addNode(edgePosition, node, node['pathCost'] + action['cost'], action['action'])


    # Monta o caminho encontrado.
    def makePath(self, node):
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


    def __str__(self):
        # Identificação das colunas
        mapa = '     ' + ' '.join("{:03}".format(i) for i in range(self.field.shape[1])) + '\n'

        for i, line in enumerate(self.field.field):

            mapa += "{:03} ".format(i)
            for j, pos in enumerate(line):
                try:
                    mapa += "| " + ('G' if self.node[(i, j)]['isGoal'] else 'V' if self.node[(i, j)]['visited'] else 'U') + " "
                except:
                    mapa += "|   "

            mapa += '\n'


        
        return mapa
