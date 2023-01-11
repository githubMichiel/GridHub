"""
battery.py

- Contains the battery class used for solving the SmartGrid problem.
"""

class Battery:
    """" store information about the batteries in the grid"""

    def __init__(self, x, y, capacity):
        """ create batteries"""

        self.x = x
        self.y = y
        self.capacity = capacity

        # location of the battery
        self.location = f"{self.x},{self.y}"
