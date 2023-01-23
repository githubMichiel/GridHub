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
        self.unique_cables_list = []

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
        """check if all houses are connected. if not, clear connections to batteries"""
        for house in self.houses:
            if house.battery == None:
                return False
        return True

    def clear_connections(self):
        """clear connections if not all houses are connected"""

        # reset house stats
        for house in self.houses:
            house.battery == None
            house.cables = []

        # reset batterie stats
        for battery in self.batteries:
            battery.total_input = 0
            battery.houses = []

    def random_connect(self):
        """algorithm to connect houses with batteries randomly"""

        for house in self.houses:
            # choose a random battery
            random.shuffle(self.batteries)

            # create battery-house connection
            for battery in self.batteries:
                    if battery.check_capacity_limit(house.max_output):
                        house.set_battery(battery)
                        battery.add_input(house.max_output)
                        break

        # return true if all houses are connected
        return self.all_houses_connected()

    def check_capacity_constraint(self):
        """check if capacity constraint is met for all batteries"""

        for batteries in self.batteries:
            # print("input", batteries.total_input)
            # print("capacity", batteries.capacity, "\n")
            if batteries.total_input > batteries.capacity:
                return False
        return True

    def connect_house_battery(self, is_random_algorithm):
        """ connect each house to a battery depending on the chosen algorithm"""

        # option 1: implement random cable connection
        if is_random_algorithm == True:
            is_all_connected = self.random_connect()

            # continue until all houses are connected
            while is_all_connected == False:
                self.clear_connections()
                is_all_connected = self.random_connect()

        # option 2: implement greedy cable connection (to closest battery)
        else:
            # sort houses based on output level
            self.houses.sort(key=lambda x: x.max_output, reverse=True)

            # loop over all (or x amount of) houses
            count_connected_houses = 0

            for house in self.houses:
                # determine closest battery and insert battery object
                closest_battery = None
                # maximum distance is 100
                shortest_distance = 101

                # loop over all batteries to search for shortest distance
                for battery in self.batteries:
                    if battery.check_capacity_limit(house.max_output):
                        current_distance = self.calculate_distance(house, battery)

                        # if shorter distance and if adequate capacity set to current battery
                        if current_distance < shortest_distance:
                            shortest_distance = current_distance
                            closest_battery = battery

                # connect closest available battery to house
                if closest_battery != None:
                    house.set_battery(closest_battery)
                    closest_battery.add_input(house.max_output)
                    count_connected_houses += 1

            print(f"Total connected houses step 1: {count_connected_houses}")
            if count_connected_houses != 150:
                print("NOT 150 houses")



            # check battery input before swap
            for battery in self.batteries:
                print(f"Battery {battery.id} input before swap: {battery.total_input}")

            print(f"Total connected houses step 1: {count_connected_houses}")

            # keep track of unconnected houses
            unconnected_houses = []
            for house in self.houses:
                if house.battery == None:
                    unconnected_houses.append(house)

            print("list of unconnected houses: ", unconnected_houses)
            for house in unconnected_houses:
                print("output of unconnected house: ", house.max_output)

            # in case not all houses are connected swap batteries
            if count_connected_houses != 150:
                while count_connected_houses != 150:
                    houses_index = range(100, 148)

                    for x in houses_index:
                        swap_buddy = random.choice(houses_index)
                        while x == swap_buddy:
                            swap_buddy = random.choice(houses_index)

                        # swap battery of two houses
                        self.houses[x].swap_battery(self.houses[swap_buddy])
                        if self.houses[x].battery.total_input > self.houses[x].battery.capacity or self.houses[swap_buddy].battery.total_input > self.houses[swap_buddy].battery.capacity:
                            # print("capacity limit - swap back")
                            self.houses[x].swap_battery(self.houses[swap_buddy])

                        for battery in self.batteries:
                            free_space = battery.capacity - battery.total_input
                            for house in unconnected_houses:
                                if free_space >= house.max_output:
                                    house.set_battery(battery)
                                    battery.add_input(house.max_output)
                                    count_connected_houses += 1
                                    unconnected_houses.remove(house)


            unconnected_houses = []
            for house in self.houses:
                if house.battery == None:
                    unconnected_houses.append(house)
            print("list of unconnected houses step 2: ", unconnected_houses)
            print(f"Total connected houses step 2: {count_connected_houses}")

            for battery in self.batteries:
                print(f"Battery {battery.id} input before swap: {battery.total_input}")

            if self.check_capacity_constraint() is not True:
                print("Capacity constraint is NOT met")

    def list_houses_per_battery(self):
        """create a list of all connected houses per battery"""

        for battery in self.batteries:
            for house in self.houses:
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

    # if the cables can be shared we remove duplicates from the list of all cables of the district
    # DOES NOT WORK YET WITH CABLE CLASS INSTEAD OF CABLE TUPLES
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
        print(len(self.all_cables))

    def make_dict_district_batteries(self):
        """make dictionary consisting of batteries (keys) and its connected houses in a list (values)"""

        for battery in self.batteries:
            self.batteries_houses[battery] = battery.houses
