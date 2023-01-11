"""
battery.py

- Contains the battery class used for solving the SmartGrid problem.
"""

class Battery:
    """" store information about the batteries in the grid"""

    def __init__(self, id, x, y, capacity):
        """ create batteries"""

        self.id = id
        self.x = x
        self.y = y
        self.capacity = capacity
