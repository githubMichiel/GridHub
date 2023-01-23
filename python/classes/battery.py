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
        self.houses = []

        # keep track of battery input
        self.total_input = 0

    def __repr__(self):
        """JSON representation of a battery object"""

        return f'"location": "{self.x},{self.y}","capacity": {self.capacity},"houses": {self.houses}'

    def add_input(self, input):
        """add new input to battery"""

        self.total_input += input

    def check_capacity_limit(self, input):
        """check if new connection to this battery can be made without exceeding the capacity"""

        new_input = input + self.total_input
        if new_input < self.capacity:
            return True
        else:
            return False

    def print_input(self):
        """testing and debugging"""
        
        print(f" Total input of battery: {self.total_input}")
