"""
cable.py

- Contains the cable class used for solving the SmartGrid problem.
"""

class Cable:
    """store information about the cables in the grid"""

    def __init__(self, start_x, start_y, end_x, end_y):
        """create cable"""
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)

    def __repr__(self):
        """JSON representation of a cable object"""

        return f'"{self.start[0]},{self.start[1]}"'
