"""
Cost functions
"""
import numba as nb
import numba.typed as typed

__all__ = ['manhattanDistance', 'chebyshevDistance', 'euclideanDistance', 'crossDistance']


def AStar(start, goal, node):
    return node['pathCost'] + manhattanDistance(goal, node['position'])


def uniform(start, goal, node):
    return node['pathCost']


def greedy(start, goal, node):
    return manhattanDistance(goal, node['position'])


def AStarDirect(start, goal, node):
    refX, refY = goal
    startGoal = (start[0] - refX, start[1] - refY)
    nodeGoal = (node['position'][0] - refX, node['position'][1] - refY)

    return (
        node['pathCost'] + manhattanDistance(goal, node['position'])
        + 0.0001*crossDistance(nodeGoal, startGoal)
    )


"""
Heuristics
"""
# Distância de Manhattan
# Considera apenas 4 movimentos possíveis em uma grade.
@nb.njit(nb.float64(nb.types.UniTuple(nb.int64, 2), nb.types.UniTuple(nb.int64, 2)))
def manhattanDistance(position1, position2):
    return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


# Distância de Chebyshev
# Considera 8 movimentos possíveis em uma grade.
@nb.njit(nb.float64(nb.types.UniTuple(nb.int64, 2), nb.types.UniTuple(nb.int64, 2)))
def chebyshevDistance(position1, position2):
    return max((abs(position1[0] - position2[0]), abs(position1[1] - position2[1])))


# Distância Euclidiana
# Calcula o comprimento da linha reta que conecta dois pontos.
@nb.njit(nb.float64(nb.types.UniTuple(nb.int64, 2), nb.types.UniTuple(nb.int64, 2)))
def euclideanDistance(position1, position2):
    return ((position1[0] - position2[0])**2 + (position1[1] - position2[1])**2)**0.5


# Distância "Produto vetorial"
# Calcula o valor do produto vetorial entre dois vetores
# Pode ser utilizado para compor heurística com um vetor ligando o ponto atual
# ao objetivo e outro vetor ligando a origem ao objetivo.
@nb.njit(nb.float64(nb.types.UniTuple(nb.int64, 2), nb.types.UniTuple(nb.int64, 2)))
def crossDistance(vector1, vector2):
    return abs(vector1[0]*vector2[1] - vector2[0]*vector1[1])
