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
        return f'"location": "{self.x},{self.y}","capacity": {self.capacity},"houses": {self.houses}'

    # add new input to battery
    def add_input(self, input):
        self.total_input += input

    # check if new connection to this battery can be made with exceeding the capacity
    def check_capacity_limit(self, input):
        new_input = input + self.total_input
        if new_input < self.capacity:
            return True
        else:
            return False


    def print_input(self):
        print(f" Total input of battery: {self.total_input}")
