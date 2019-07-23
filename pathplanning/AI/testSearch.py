import numpy as np
import numba as nb

import heapq
import math

from .graph2D import Graph2D


"""
Algoritmos de busca para encontrar o caminho que minimiza um determiando custo entre dois pontos.
"""
class TestSearch:
    # Verifica se existe a linha reta que liga dois pontos.
    # Se a linha não existir, retorna a posição do obstáculo.
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
