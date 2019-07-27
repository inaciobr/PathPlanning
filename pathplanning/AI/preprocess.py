"""
Algoritmos de pré-processamento do mapa.
"""
import numba as nb
import numpy as np

from collections import deque


__all__ = ['allowedMoves', 'waveVector', 'connectedComponent', 'floydWarshall']


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


# Distância em 4 movimentos entre dois pontos
@nb.njit(nb.int64[:, :, :](nb.types.UniTuple(nb.int64, 2), nb.boolean[:, :]))
def waveVector(source, mask):
  moves = [(0, 0, 0, 1), (0, 0, 1, 0), (0, 1, 0, 0), (1, 0, 0, 0)]
  limX, limY = mask.shape

  wave = np.full((*mask.shape, 4), -1, dtype=np.int64)
  wave[source] = 0, 0, 0, 0

  i = 0
  frontier = [ source ]
  
  while i < len(frontier):
      posX, posY = frontier[i]
      i += 1

      for u, d, l, r in moves:
          edge = posX + u - d, posY + r - l

          if wave[edge][0] == -1 and 0 <= edge[0] < limX and 0 <= edge[1] < limY and mask[edge]:
              wave[edge][0] = wave[posX, posY][0] + u
              wave[edge][1] = wave[posX, posY][1] + d
              wave[edge][2] = wave[posX, posY][2] + l
              wave[edge][3] = wave[posX, posY][3] + r
              frontier.append(edge)

  return wave.astype(np.uint64)






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
    dist = np.empty((*field.shape, *field.shape), dtype = np.float64)

    for i in nb.prange(dist.shape[0]):
        for j in nb.prange(dist.shape[1]):
            for u in nb.prange(dist.shape[2]):
                for v in nb.prange(dist.shape[3]):
                    dist[i, j, u, v] = \
                        0.0 if i == u and j == v else \
                        1.0 if (i - u == 1 or i - u == -1) and (j == v) or \
                               (j - v == 1 or j - v == -1) and (i == u) else \
                        np.inf

    # Iteração
    for i, j, k in np.ndindex((field.size, field.size, field.size)):
        if dist[i, j] > dist[i, k] + dist[k, j]:
            dist[i, j] = dist[i, k] + dist[k, j]

    # Reshape para 4-dim
    return dist
