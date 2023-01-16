import numpy as np
from battery import Battery
from house import House
import csv
import random

class District:

    def __init__(self, id, is_unique):
        self.id = id
        self.batteries = []
        self.houses = []
        self.costs = 25000
        self.total_cables = []

        # boolean: True if the cables are unique, False if cables can be shared
        self.is_unique = is_unique
        if self.is_unique:
            self.unique_cables = 'costs-own'
        else:
            self.unique_cables = 'costs-shared'

    def load_batteries(self, filename):
        """ load batteries into memory"""

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
                # right now each battery is connected to 2 houses based on its x and y coordinates just for json output testing
                battery = Battery(id, x, y, capacity)
                self.batteries.append(battery)
                id += 1


    def load_houses(self, filename):
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

#    def __repr__(self):
#        return f'"district": {self.id},"{self.unique_cables}": {self.costs}'

    def connect_house_battery(self):
        """ connect each house to a random battery"""
        for house in self.houses:

            # choose a random battery
            random.shuffle(self.batteries)

            for battery in self.batteries:
                if battery.check_capacity_limit(house.max_output):
                    house.set_battery(battery)
                    house.add_connection(battery)
                    break

    # add all of the cables that are stored in all of the houses to the list of all cables of the district
    def add_all_cables(self):
        for house in self.houses:
            for cables in house.cables:
                self.total_cables.append(house.cables)

    # if the cables can be shared we remove duplicates from the list of all cables of the district
    def remove_duplicate_cables(self):
        if self.is_unique == False:
