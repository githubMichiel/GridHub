"""
district.py

- Contains the district class used for solving the SmartGrid problem.
"""

import numpy as np
import csv
import random

from .battery import Battery
from .house import House
from .cable import Cable

class District:
    """create a District object which stores House, Battery and Cable objects
    and performs operations with them"""

    def __init__(self, id, is_unique):
        """create districts"""

        self.id = id

        # list of battery objects in district
        self.batteries = []

        # list of house objects in district
        self.houses = []

        # total costs of all cables and batteries in district; start at 25000 i.e. costs of all batteries
        self.costs = 0

        # dictionary with all batteries as keys and a list of connected houses per battery as values
        self.batteries_houses = {}

        # list of all of the cables in district
        self.all_cables = []

        # boolean is True if cables are unique, False if cables are shared
        self.is_unique = is_unique
        if self.is_unique:
            self.unique_cables = 'costs-own'
        else:
            self.unique_cables = 'costs-shared'

    def load_batteries(self, filename):
        """load batteries into memory"""

        with open(filename, "r") as f:
            csvreader = csv.reader(f)

            # skip first line
            next(csvreader)

            id = 1
            for row in csvreader:
                x = int(row[0])
                y = int(row[1])
                capacity = float(row[2])

                # create battery
                battery = Battery(id, x, y, capacity)
                self.batteries.append(battery)
                id += 1

    def load_houses(self, filename):
        """load houses into memory"""

        with open(filename) as f:
            csvreader = csv.reader(f)

            # skip first line
            next(csvreader)

            for row in csvreader:
                x = int(row[0])
                y = int(row[1])
                max_output = float(row[2])

                # create house
                house = House(x, y, max_output)
                self.houses.append(house)

    def __repr__(self):
        """JSON representation of district object"""

        return f'"district": {self.id},"{self.unique_cables}": {self.costs}'

    def calculate_distance(self, house, battery):
        """calculate the Manhattan distance between house and battery"""

        distance = 0
        distance += abs(house.x - battery.x)
        distance += abs(house.y - battery.y)
        return distance

    def all_houses_connected(self):
        """check if all houses are connected, if so return True"""
        for house in self.houses:
            if house.battery == None:
                return False
        return True

    def clear_connections(self):
        """clear connections if not all houses are connected"""

        # reset house stats
        for house in self.houses:
            house.battery = None
            house.cables = []

        # reset battery stats
        for battery in self.batteries:
            battery.total_input = 0
            battery.houses = []

    def check_capacity_constraint(self):
        """check if capacity constraint is met for all batteries"""

        for batteries in self.batteries:
            if batteries.total_input > batteries.capacity:
                return False
        return True

    def list_houses_per_battery(self):
        """create a list of all connected houses per battery"""

        for house in self.houses:
            for battery in self.batteries:
                if battery is house.battery:
                    battery.houses.append(house)

    def add_all_cables(self):
        """add all cables that are stored in all houses to a list of all cables (per district)"""

        for house in self.houses:
            for i in range(len(house.cables)):
                self.all_cables.append(house.cables[i])

    def calculate_total_costs(self):
        """calculate the total cost of a district with cables"""

        number_of_cables = len(self.all_cables) - len(self.houses)
        self.costs = (len(self.batteries) * 5000) + (number_of_cables * 9)
        return self.costs

    def reset_costs(self):
        """reset the costs and cables in a district"""
        self.costs = 0
        self.all_cables = []

    def remove_duplicate_cables(self):
        """remove duplicate cables per grid segment"""

        unique_cables = set()
        new_cable_list = []

        print(len(self.all_cables))
        # loop over cables
        for cable in self.all_cables:
            next_cable_1 = (cable.start, cable.end)
            next_cable_2 = (cable.end, cable.start)

            # check if cable is duplicate
            if next_cable_1 not in unique_cables and next_cable_2 not in unique_cables:
                new_cable_list.append(cable)
                unique_cables.add(next_cable_1)

        self.all_cables = new_cable_list
