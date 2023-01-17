import numpy as np
from battery import Battery
from house import House
from cable import Cable
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

    def __repr__(self):
         return f'"district": {self.id},"{self.unique_cables}": {self.costs}'

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


    def __repr__(self):
        return f'"district": {self.id},"{self.unique_cables}": {self.costs}'


    # calculate the Manhattan distance between house and battery
    def calculate_distance(self, house, battery):
        distance = 0
        distance += abs(house.x - battery.x)
        distance += abs(house.y - battery.y)
        return distance

    # check if all houses are connected, if not clear connections to batteries
    def all_connected(self):
        for house in self.houses:
            if house.battery == None:
                self.clear_connections()
                return False
        return True

    # clear connections if not all houses are connected
    def clear_connections(self):
        for house in self.houses:
            house.battery == None
            house.cables = []
        for battery in self.batteries:
            battery.total_input = 0
            battery.houses = []

    # random algorithm to connect houses with batteries randomly
    def random_connect(self):
        for house in self.houses:
            # choose a random battery
            random.shuffle(self.batteries)

            # create battery-house connection
            for battery in self.batteries:
                    if battery.check_capacity_limit(house.max_output):
                        house.set_battery(battery)
                        house.add_connection(battery)
                        battery.add_input(house.max_output)
                        break

        # return true if all houses are connected
        return self.all_connected()

    def connect_house_battery(self, argv):
        """ connect each house to a random battery"""
        # option 1: implement random cable connection
        if argv == 1:
            is_all_connected = self.random_connect()
            while is_all_connected == False:
                is_all_connected = self.random_connect()

        # option 2: implement cable connection to closest battery
        else:
            for house in self.houses:
                # determine closest battery and insert battery object
                closest_battery = None
                # maximum distance is 100
                shortest_distance = 101

                    # random.shuffle(self.batteries)

                    # loop over all batteries to search for shortest distance
                for battery in self.batteries:
                    if battery.check_capacity_limit(house.max_output):
                        current_distance = self.calculate_distance(house, battery)

                        # if shorter distance and if adequate capacity set to current battery
                        if current_distance < shortest_distance:
                            shortest_distance = current_distance
                            closest_battery = battery

                # connect closest available battery to house
                house.set_battery(closest_battery)
                house.add_connection(closest_battery)
                closest_battery.add_input(house.max_output)





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
        self.costs = (len(self.batteries) * 5000) + (len(self.all_cables) * 9)

    # if the cables can be shared we remove duplicates from the list of all cables of the district
    # DOES NOT WORK YET WITH CABLE CLASS INSTEAD OF CABLE TUPLES
    #def remove_duplicate_cables(self):
    #    if self.is_unique == False:
    #        self.all_cables = list(set(self.all_cables))

    # make dictionary consisting of batteries (keys) and its connected houses in a list (values)
    def make_dict_district_batteries(self):
        for battery in self.batteries:
            self.batteries_houses[battery] = battery.houses
