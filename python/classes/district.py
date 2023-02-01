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

        # total costs of all cables and batteries in district
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
            # read line
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

            # read line
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

    def clear_connections(self, cables_only):
        """clear connections if not all houses are connected"""

        # sometimes only the cable connections should be removed
        if cables_only:
            for house in self.houses:
                house.cables = []
            for battery in self.batteries:
                battery.houses = []

        # otherwise clear all connections
        else:
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
                # print("house.cables", house.cables)
                self.all_cables.append(house.cables[i])

    def calculate_total_costs(self):
        """calculate the total cost of a district with cables"""

        # calculate # of cables
        number_of_cables = len(self.all_cables) - len(self.houses)

        # calculate cost
        self.costs = (len(self.batteries) * 5000) + (number_of_cables * 9)

        # return costs
        return self.costs

    def reset_costs(self):
        """reset the costs and cables in a district"""

        self.costs = 0
        self.all_cables = []

    def remove_duplicate_cables(self):
        """remove duplicate cables per grid segment"""

        unique_cables = set()
        new_cable_list = []

        # loop over all cables in a district
        for cable in self.all_cables:
            # cable that should be checked (and its reverse)
            next_cable_1 = (cable.start, cable.end)
            next_cable_2 = (cable.end, cable.start)

            # check if cable is duplicate
            if next_cable_1 not in unique_cables and next_cable_2 not in unique_cables:
                # add cable to new list if not yet in that list
                new_cable_list.append(cable)
                unique_cables.add(next_cable_1)

        # update the list of all cables in a district
        self.all_cables = new_cable_list

        # cables should be removed inside the house objects as well
        unique_cables_2 = set()
        # list of lists of cables
        new_cable_matrix = []

        # loop over houses in a district
        for i in range(150):
            # create new list of cables per house
            new_cable_matrix.append([])
            # loop over cables in a house
            for cable in self.houses[i].cables:
                # cable that should be checked (and its reverse)
                next_cable_1 = (cable.start, cable.end)
                next_cable_2 = (cable.end, cable.start)

                # check if cable is duplicate
                if next_cable_1 not in unique_cables_2 and next_cable_2 not in unique_cables_2:
                    # add cable to new list if not yet in that list
                    new_cable_matrix[i].append(cable)
                    unique_cables_2.add(next_cable_1)

        for i in range(150):
            self.houses[i].cables = new_cable_matrix[i]

        print(new_cable_matrix)
        print(self.houses[i].cables)
