import random
from ..visualizations.visualize import plot_district

class Greedy():
    """algorithm to connect houses with batteries with greedy heuristic.
    runs until a valid solution is found."""

    def __init__(self, district, UNIQUE_CABLES):
        """ initialize greedy object"""

        # list of districts on which to perform the algorithm
        self.district = district

        # algorithm changes if cables are unique vs. shared
        self.UNIQUE_CABLES = UNIQUE_CABLES

        # keep track of how many houses are connected
        self.total_connected_houses = 0

    def connect_closest_battery(self, district):
        """ greedily connects houses to the closest battery"""

        # sort houses based on output level (used for experimenting)
        # district.houses.sort(key=lambda x: x.max_output, reverse=True)

        # randomise houses order
        random.shuffle(district.houses)

        # loop over all (or x amount of) houses
        for house in district.houses:
            # determine closest battery and insert battery object
            closest_battery = None
            # maximum distance is 100
            shortest_distance = 101

            # loop over all batteries to search for shortest distance
            for battery in district.batteries:
                # only connect to battery if sufficient capacity
                if battery.check_capacity_limit(house.max_output):
                    current_distance = district.calculate_distance(house, battery)

                    # if shorter distance and if adequate capacity set to current battery
                    if current_distance < shortest_distance:
                        shortest_distance = current_distance
                        closest_battery = battery

            # connect closest available battery to house
            if closest_battery != None:
                house.set_battery(closest_battery)
                closest_battery.add_usage(house.max_output)

                # when a house is connected this should be updated
                self.total_connected_houses += 1

    def unconnected_houses(self, district):
        """ creates a list of houses that are not connected to a battery"""

        unconnected_houses = []
        for house in district.houses:
            if house.battery == None:
                unconnected_houses.append(house)

        return unconnected_houses

    def swap_houses(self, district, unconnected_houses, search_free_space, swap_index, swap_once):
        """ swaps the battery connection of two houses
        swap until capacity constraint is met
        return True if succesful swap"""

        # swap index decides in which range of houses you want to swap
        if swap_index == 1:
            houses_index = range(100, 148)
        elif swap_index == 2:
            houses_index = range(0, 149)

        # find a house to swap with
        for x in houses_index:
            swap_buddy = random.choice(houses_index)
            # cannot swap the same house
            while x == swap_buddy:
                swap_buddy = random.choice(houses_index)

            # swap battery of two houses
            district.houses[x].swap_battery(district.houses[swap_buddy])

            # if battery capacity is exceeded swap back
            swap_occurred = False

            # can only swap houses that are connected to a battery
            if district.houses[x].battery != None and district.houses[swap_buddy].battery != None:
                # if house input exceeds battery capacity
                if district.houses[x].battery.total_input > district.houses[x].battery.capacity or district.houses[swap_buddy].battery.total_input > district.houses[swap_buddy].battery.capacity:
                    # swap back
                    district.houses[x].swap_battery(district.houses[swap_buddy])
                    # depending on configuration you want to swap once
                    if swap_once == True:
                        return swap_occurred

                # otherwise swap was succesfull
                else:
                    swap_occurred = True
                    if swap_once == True:
                        return swap_occurred

            # if there is free space and a swap has occurred
            if search_free_space == True and swap_occurred == True:
                # loop over batteries
                for battery in district.batteries:
                    # calculate available battery space
                    free_space = battery.capacity - battery.total_input

                    # connect each house to battery if sufficient capacity
                    for house in unconnected_houses:
                        if free_space >= house.max_output:
                            house.set_battery(battery)
                            battery.add_usage(house.max_output)
                            self.total_connected_houses += 1
                            unconnected_houses.remove(house)

                            # if no unconnected houses
                            if len(unconnected_houses) == 0:
                                return swap_occurred

        # return bool if swap occurred or not
        return swap_occurred

    def remove_cable_connections(self, district):
        """remove all cable connections but keep in memory which house is connected to which battery"""

        #remove cables from houses
        for house in district.houses:
            house.cables = []

        #remove cables from district
        district.all_cables = []

    def add_efficient_cables(self, district):
        """add cables in a more efficient way using a heuristic:
        connect houses to the closest available cable.
        (instead of closest available battery)"""

        # loop over all batteries to add cables BUT more efficient
        for battery in district.batteries:

            # calculate distances between house and batteries
            for house in battery.houses:
                house.distance_to_batt = district.calculate_distance(house, battery)

            # sort houses based on distance to battery; closest house first
            battery.houses.sort(key=lambda x: x.distance_to_batt)

            # make list to keep track which houses are cable connected to a battery
            cable_connected_houses = []

            # loop over houses connected to that battery; start at nearest house
            for house in battery.houses:
                # connect closest house directly to battery
                if len(cable_connected_houses) == 0:
                    # add cables to house object
                    house.add_cable_connection(battery)
                    cable_connected_houses.append(house)

                # connect the other houses to the closest cable connection
                else:
                    closest_cable = None # cable object
                    closest_distance = 101
                    # loop over all cable connected houses to find the nearest cable
                    for cable_connected_house in cable_connected_houses:
                        # calculate distance from a house to an existing cable
                        for existing_cable in cable_connected_house.cables:
                            distance_house_cable = district.calculate_distance(house, existing_cable)
                            # set new closest distance and cable
                            if distance_house_cable < closest_distance:
                                # update values
                                closest_distance = distance_house_cable
                                closest_cable = existing_cable

                    # add house to closest cable
                    house.add_cable_connection(closest_cable)
                    cable_connected_houses.append(house)

    def run(self, clear_cables_only=False, search_free_space=True, swap_index=1, swap_once=False, hillclimber=False):
        """ greedily assigns houses to the closest battery
        and swap houses until the capacity constraint is met"""

        # reset district first
        self.district.reset_costs()
        self.district.clear_connections(cables_only=clear_cables_only)
        self.total_connected_houses = 0

        # connect houses to closest battery
        if not hillclimber:
            self.connect_closest_battery(self.district)

        # if not all connected, swap batteries of houses
        if not hillclimber and self.total_connected_houses != 150:
            # get list of unconnected houses
            unconnected_houses = self.unconnected_houses(self.district)
            # keep swapping until all houses are connected
            while self.total_connected_houses != 150:
                self.swap_houses(self.district, unconnected_houses, search_free_space=True, swap_index=2, swap_once=False)

        # if hillclimber is activated
        if hillclimber:
            unconnected_houses = []
            succesful_swap = self.swap_houses(self.district, unconnected_houses, search_free_space=False, swap_index=2, swap_once=True)

            # keep swapping until a swap was succesfull
            while succesful_swap is not True:
                succesful_swap = self.swap_houses(self.district, unconnected_houses, search_free_space=False, swap_index=2, swap_once=True)

        # if cables are shared
        if self.UNIQUE_CABLES == False:
            # create list of all houses connected per battery
            self.district.list_houses_per_battery()

            # add cables more efficiently
            self.add_efficient_cables(self.district)

            # add all cables into the district
            self.district.add_all_cables()

        # if cables are not shared
        elif self.UNIQUE_CABLES == True:
            # when all houses are connected AND constraints are met, add cable connections
            for house in self.district.houses:
                house.add_cable_connection(house.battery)

            # make list of connected houses per battery
            self.district.list_houses_per_battery()

            # add all cables in a district to one list
            self.district.add_all_cables()

        # return cost per district
        return self.district.calculate_total_costs()
