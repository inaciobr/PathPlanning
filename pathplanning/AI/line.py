import numba as nb

from .heuristic import Heuristic


"""
Algoritmos baseados em linhas retas
"""
class Line:
    # Verifica se existe a linha reta que liga dois pontos.
    @staticmethod
    @nb.njit(nb.boolean(nb.typeof((1, 1)), nb.typeof((1, 1)), nb.boolean[:, :]))
    def checkStraightLine(start, goal, mask):
        vecX, vecY = (goal[0] - start[0], goal[1] - start[1])
        dirX, dirY = (1 if vecX > 0 else -1, 1 if vecY > 0 else -1)
        
        stepX, stepY = (dirX * vecX, dirY * vecY)
        cross = stepY * (stepX + 0.5) + stepX * (stepY + 0.5)

        px, py = start
        i, j = 0.5*stepY, 0.5*stepX

        while i + j < cross and mask[px, py]:
            if i < j:
                px += dirX
                i += stepY
            else:
                py += dirY
                j += stepX

        return mask[px, py]


    # Algoritmo que visa puramente seguir uma linha reta.
    # Se não for possível seguir o caminho direto, ele retorna o caminho até o obstáculo
    # que interceptou o movimento.
    @staticmethod
    def straightLine(start, goal, field, actions):
        vector = (start[0] - goal[0], start[1] - goal[1])
        cost = lambda node: Heuristic.crossDistance((node[0] - goal[0], node[1] - goal[1]), vector)

        node = start
        pathCost = 0

        # Utiliza apenas as ações que apontam na direção do objetivo.
        gActions = [ act for act in actions if vector[0]*act['direction'][0] <= 0 and vector[1]*act['direction'][1] <= 0 ]

        path = [{
            'position': node,
            'pathCost': pathCost,
            'action': 'S'
        }]

        while node != goal:
            edgePos = [ (node[0] + act['direction'][0], node[1] + act['direction'][1]) for act in gActions ]
            _, node, act = min(zip(map(cost, edgePos), edgePos, gActions))

            if not field.mask[node]:
                break

            pathCost += act['cost']

            path.append({
                'position': node,
                'pathCost': pathCost,
                'action': act['action']
            })

        return path
