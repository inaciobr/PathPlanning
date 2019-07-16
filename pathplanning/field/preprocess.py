import numpy as np

class Preprocess:
    # Máscara de posições válidas
    @staticmethod
    def mask(field):
        return field != np.inf


    # Tupla com a lista das posições válidas
    @staticmethod
    def validPositions(mask):
        return mask.nonzero()


    # Separa o campo em regiões para verificar acessibilidade.
    @staticmethod
    def connectedComponent(field):
        from scipy.ndimage.measurements import label
        return label(field)[0]
