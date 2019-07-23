__all__ = ['Drone']

"""
Veículo do tipo Drone.
"""
class Drone:
    def __init__(self, label, position):
        self.label = label
        self.position = position

        self.isFlying = False
        self.goalPosition = position
        self.path = [ ]


    def turnOn(self):
        self.isFlying = True


    def turnOff(self):
        self.isFlying = False


    def setGoal(self, pos):
        self.goalPosition = pos


    def setPath(self, path):
        if path[0]['position'] != self.position:
            raise self.label + ": Trajetória inválida. Posição inicial é diferente da posição atual do drone."

        self.path = path


    def moveTo(self, pos):
        if not self.isFlying:
            raise self.label + ": O drone não está voando e não pode se mover."
        
        self.position = pos


    def __str__(self):
        return self.label
