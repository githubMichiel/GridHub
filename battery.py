"""
battery.py

- Contains the battery class used for solving the SmartGrid problem.
"""

class Battery:
    """" store information about the batteries in the grid"""

    def __init__(self, x, y, capacity, houses):
        """ create batteries"""

        self.x = x
        self.y = y
        self.capacity = capacity
        self.houses = houses

        # location of the battery
        self.location = f"{self.x}, {self.y}"

        # keep track of battery input
        self.total_input = 0

    # add new input to battery
    def add_input(self, input):
        self.total_input += input

    # check if new connection to this battery can be made with exceeding the capacity
    def check_capacity_limit(self, input):
        new_input = input + self.total_input
        if new_input < capacity:
            return True
        else:
            return False

    # string representation of a battery object that matches the json output format
    def __repr__(self):
        return f'"location": "{self.x},{self.y}","capacity": {self.capacity},"houses": {self.houses}'
