import numpy as np

"""
Implementação de do grafo 2D utilizado nos algoritmos de busca.
"""
class Graph2D:
    def __init__(self, field, actions, initialCost = 0):
        self.node = { }

        self.actions = actions
        self.field = field


    # Adiciona um novo nó ao grafo.
    def addNode(self, position, pathCost, action, parent = None):
        self.node[position] = {
            'visited': False,
            'position': position,
            'pathCost': pathCost,
            'action': action,
            'parent': parent,
        }

        return self.node[position]


    # Retorna as arestas ainda não visitadas de um nó.
    def newEdges(self, node):
        node['visited'] = True
        posX, posY = node['position']
        
        for action in self.actions:
            edgePosition = (posX + action['direction'][0], posY + action['direction'][1])

            try:
                if not self.field.mask[edgePosition] or edgePosition[0] < 0 or edgePosition[1] < 0:
                    continue
            except:
                continue

            if edgePosition in self.node:
                edgeNode = self.node[edgePosition]

                if not edgeNode['visited'] and node['pathCost'] + action['cost'] < edgeNode['pathCost']:
                    edgeNode['parent'] = node
                    edgeNode['pathCost'] = node['pathCost'] + action['cost']
                    edgeNode['action'] = action['action']
                    yield edgeNode
            else:
                yield self.addNode(edgePosition, node['pathCost'] + action['cost'], action['action'], node)


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
            for j, _ in enumerate(line):
                try:
                    mapa += "| " + ('V' if self.node[(i, j)]['visited'] else 'U') + " "
                except:
                    mapa += "|   "

            mapa += '\n'

        return mapa
