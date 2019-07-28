"""
Algoritmos de pré-processamento do mapa.
"""
import numba as nb
import numpy as np

from collections import deque


__all__ = ['allowedMoves', 'connectedComponentLabeling', 'floydWarshall']


# Movimentos permitidos
def allowedMoves(mask):
    moves = np.full(mask.shape, 0b1111, dtype = 'b')

    # 4 Movimentos
    M_UP    = 0b0001    # 0x1 -> Up
    M_DOWN  = 0b0010    # 0x2 -> Down
    M_LEFT  = 0b0100    # 0x4 -> Left
    M_RIGHT = 0b1000    # 0x8 -> Right

    # Bordas
    moves[ 0,  :] &= ~M_UP
    moves[-1,  :] &= ~M_DOWN
    moves[ :,  0] &= ~M_LEFT
    moves[ :, -1] &= ~M_RIGHT

    # Arredores dos obstáculos
    moves[1:][~mask[:-1]] &= ~M_UP
    moves[:-1][~mask[1:]] &= ~M_DOWN
    moves[:,1:][~mask[:,:-1]] &= ~M_LEFT
    moves[:,:-1][~mask[:,1:]] &= ~M_RIGHT

    # Obstáculos
    moves[~mask] = 0b0000

    return moves


# Connected Component Labeling
# Obstáculos têm valor 0.
@nb.njit(nb.int64[:,:](nb.boolean[:, :]))
def connectedComponentLabeling(mask):
    linked = [ 0 ]
    labels = np.zeros(mask.shape, dtype = np.int64)
    nextLabel = 1

    # First pass
    for i, j in np.ndindex(mask.shape):
        if not mask[i, j]:
            continue

        n1 = labels[i - 1, j] if i > 0 else 0
        n2 = labels[i, j - 1] if j > 0 else 0

        # Has neighbors
        if n1 or n2:
            labels[i, j] = n1 if n1 > n2 else n2

            # Union
            if n1 and n2 and n1 != n2:
                a, b = n1, n2

                while linked[a] != a:
                    a = linked[a]
                while linked[b] != b:
                    b = linked[b]

                minLabel = a if a < b else b
                linked[b] = linked[a] = minLabel

                # Merge
                a, b = n1, n2
                while a != minLabel:
                    a, linked[a] = linked[a], minLabel
                while b != minLabel:
                    b, linked[b] = linked[b], minLabel

        # Doesn't have neighbors
        else:
            labels[i, j] = nextLabel
            linked.append(nextLabel)
            nextLabel += 1

    # Normalization of the labels
    norm = 0
    for i, link in enumerate(linked):
        if i == link:
            linked[i] = norm
            norm += 1
        else:
            linked[i] = linked[link]
            
    # Second pass
    for i, j in np.ndindex(mask.shape):
        if mask[i, j]:
            labels[i, j] = linked[labels[i, j]]

    return labels


# Algoritmo de Floyd-Warshall
@nb.njit(nb.float32[:, :, :, :](nb.boolean[:, :]), parallel = True)
def floydWarshall(mask):
    dist = np.empty((*mask.shape, *mask.shape), dtype = np.float32)

    for i in nb.prange(dist.shape[0]):
        for j in nb.prange(dist.shape[1]):
            for u in nb.prange(dist.shape[2]):
                for v in nb.prange(dist.shape[3]):
                    dist[i, j, u, v] = \
                        0.0 if i == u and j == v else \
                        mask[i, j]| mask[u, v] \
                            if (i - u == 1 or i - u == -1) and (j == v) or \
                               (j - v == 1 or j - v == -1) and (i == u) else \
                        np.inf
    
    dist = dist.reshape((mask.size, mask.size))
    for i, j in np.ndindex(dist.shape):
        dist[i, j] = np.min(dist[i, :] + dist[:, j])

    # Reshape para 4-dim
    return dist.reshape((*mask.shape, *mask.shape))
