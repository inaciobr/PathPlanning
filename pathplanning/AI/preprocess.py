"""
Algoritmos de pré-processamento do mapa.
"""
import numba as nb
import numpy as np

__all__ = ['connectedComponent', 'floydWarshall', 'waveVector']


# Connected Component Labeling
# Obstáculos têm valor 0.
#@nb.njit(nb.int64[:,:](nb.boolean[:, :]))
def connectedComponent(mask):
    linked = [ set(0) ]
    labels = np.zeros(mask.shape, dtype = np.int64)
    nextLabel = 1

    # First pass
    for i, j in np.ndindex(mask.shape):
        if not mask[i, j]:
            pass

        n1 = labels[i - 1, j] if i > 0 else 0
        n2 = labels[i, j - 1] if j > 0 else 0

        if n1 or n2:
            labels[i, j] = n1 if n1 > n2 else n2

            if n1 and n2:
                linked[n1].add(n2)
                linked[n2].add(n1)

        else:
            linked.append(set(nextLabel))
            labels[i, j] = nextLabel
            nextLabel += 1


    # Second pass
    for i, j in np.ndindex(mask.shape):
        if mask[i, j]:
            for label, s in linked:
                if labels[i, j] in s:
                    labels[i, j] = label

    return labels

    
# Algoritmo de Floyd-Warshall
def floydWarshall(field):
    dist = np.full((field.size, field.size), np.inf)

    # Diagonal principal = 0
    dist[np.arange(field.size), np.arange(field.size)] = 0

    # Nós vizinhos:

    for i, j, k in np.ndindex((field.size, field.size, field.size)):
        if dist[i, j] > dist[i, k] + dist[k, j]:
            dist[i, j] = dist[i, k] + dist[k, j]

    # Reshape para 4-dim
    return dist


# Algoritmo de Floyd-Warshall
def waveVector(field):
    pass


# Movimentos permitidos
def allowedMoves(mask):
    pass