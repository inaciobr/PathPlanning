

__all__ = ['Drone']

"""
Veículo do tipo Drone.
"""
class Drone:
    def __init__(self, label, position):
        self.label = label
        self.isFlying = False

        self.position = position
        self.goalPosition = position

        self.path = [ ]


    def __repr__(self):
        return self.label


    def __dict__(self):
        return {
            'label': self.label,
            'isFlying': self.isFlying,
            'position': self.position,
            'goalPosition': self.goalPosition,
            'path': self.path
        }
