"""
Heuristics
"""
class Heuristic:
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
