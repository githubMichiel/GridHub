"""
cable.py

- Contains the cable class used for solving the SmartGrid problem.
"""

class Cable:
    """store information about the cables in the grid"""

    def __init__(self, x, y):
        """create cable"""

        self.x = x
        self.y = y

    def __repr__(self):
        """JSON representation of a cable object"""

        return f'"{self.x},{self.y}"'
