import numpy as np
from battery import Battery
from house import House
import csv
import random

class District:

    def __init__(self, id, is_unique):
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

    # make list of connected houses per battery
    def list_houses_battery(self):
        for battery in self.batteries:
            for house in self.houses:
                if battery is house.battery:
                    battery.houses.append(house)

    # add all of the cables that are stored in all of the houses to the list of all cables of the district
    def add_all_cables(self):
        for house in self.houses:
            for i in range(len(house.cables)):
                self.all_cables.append(house.cables[i])

    def total_costs(self):
        number_of_cables = len(self.all_cables) - len(self.houses)
        self.costs = (len(self.batteries) * 5000) + (number_of_cables * 9)

    # if the cables can be shared we remove duplicates from the list of all cables of the district
    def remove_duplicate_cables(self):
        if self.is_unique == False:
            self.all_cables = list(set(self.all_cables))

    # make dictionary consisting of batteries (keys) and its connected houses in a list (values)
    def make_dict_district_batteries(self):
        for battery in self.batteries:
            self.batteries_houses[battery] = battery.houses

    # calculate the Manhattan distance between house and battery
    def calculate_distance(self, house, battery):
        distance = 0
        distance += abs(house.x - battery.x)
        distance += abs(house.y - battery.y)
        return distance
