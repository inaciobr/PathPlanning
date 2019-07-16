__all__ = ['Drone']

"""
Veículo do tipo Drone.
"""
class Drone:
    actions = [
        { 'action': '^', 'cost': 1, 'direction': (-1,  0), 'hash': 0x01 },
        { 'action': 'v', 'cost': 1, 'direction': (+1,  0), 'hash': 0x02 },
        { 'action': '<', 'cost': 1, 'direction': ( 0, -1), 'hash': 0x04 },
        { 'action': '>', 'cost': 1, 'direction': ( 0, +1), 'hash': 0x08 },
        #{'action': 'o', 'cost': 1, 'direction': ( 0,  0), 'hash': 0x10 },
    ]

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


    def setGoalPosition(self, pos):
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
