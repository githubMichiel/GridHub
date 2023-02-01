"""
house.py

- Contains the house class used for solving the SmartGrid problem.
"""

from .cable import Cable

class House():
    """create a House object that stores information about houses in a district"""

    def __init__(self, x, y, max_output):
        """create houses"""

        self.x = x
        self.y = y
        self.max_output = max_output

        # remember to which battery a house is connected
        self.battery = None

        # remember the distance to a battery
        self.distance_to_batt = None

        # make list with cable location from house to battery
        self.cables = []

    def __repr__(self):
        """JSON representation of house object"""

        return f'{{"location": "{self.x},{self.y}","output": {self.max_output},"cables": {self.cables}}}'

    def set_battery(self, battery):
        """connect house to a battery object"""

        self.battery = battery

    def swap_battery(self, other):
        """ swap batteries of two houses"""

        # swap the batteries of two houses
        if self.battery != None and other.battery != None:
            # switch output for first battery
            self.battery.total_input -= self.max_output
            self.battery.total_input += other.max_output

            # switch output for second battery
            other.battery.total_input -= other.max_output
            other.battery.total_input += self.max_output

            # switch the self.battery for both houses
            self.battery, other.battery = other.battery, self.battery

    def add_cable_connection(self, battery):
        """add cable connection between house and battery.
        chooses the shortest route.
        (this algorithm is for the unique cable case where it doesnt matter what shortest route we pick)"""

        self.cables = []

        # calculate distance along x and y axis
        distance_x = self.x - battery.x
        distance_y = self.y - battery.y

        # horizontally: house is to the right of the battery
        if distance_x >= 0:
            for i in range(abs(distance_x)):
                self.cables.append(Cable(self.x - i, self.y, self.x - (i+1), self.y ))

        # horizontally: house is to the left of the battery
        else:
            for i in range(abs(distance_x)):
                self.cables.append(Cable(self.x + i, self.y, self.x + (i+1), self.y))

        # vertically: house is above the battery
        if distance_y >= 0:
            for i in range(abs(distance_y)):
                self.cables.append(Cable(self.x - distance_x, self.y - i, self.x - distance_x, self.y - (1+i)))

        # vertically: house is below the battery
        else:
            for i in range(abs(distance_y)):
                self.cables.append(Cable(self.x - distance_x, self.y + i, self.x - distance_x, self.y + (i+1)))
        self.cables.append(Cable(battery.x,battery.y,battery.x,battery.y))
