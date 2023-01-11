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
        self.location = f"{self.x}, {self.y}"

        # keep track of battery input
        self.totalinput = 0

    # add new input to battery
    def add_input(self, input):
        self.totalinput += input

    # check if new connection to this battery can be made with exceeding the capacity
    def check_connection(self, input):
        newinput = input + self.totalinput
        if newinput < capacity:
            return True
        else:
            return False
