import random

class Greedy():
    """algorithm to connect houses with batteries with greedy heuristic.
    runs until a valid solution is found."""

    def __init__(self, districts, UNIQUE_CABLES):

        # list of districts on which to perform the algorithm
        self.districts = districts

        # algorithm changes if cables are unique vs. shared
        self.UNIQUE_CABLES = UNIQUE_CABLES

        # keep track of how many houses are connected
        self.total_connected_houses = 0

    def connect_closest_battery(self, district):
        """ greedily connects houses to the closest battery"""

        # option 2: implement greedy cable connection (to closest battery)
        # sort houses based on output level
        district.houses.sort(key=lambda x: x.max_output, reverse=True)

        # loop over all (or x amount of) houses
        for house in district.houses:
            # determine closest battery and insert battery object
            closest_battery = None
            # maximum distance is 100
            shortest_distance = 101

            # loop over all batteries to search for shortest distance
            for battery in district.batteries:
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

    def swap_houses(self, district, unconnected_houses):
        """ swaps the battery connection of two houses
        swap until capacity constraint is met."""

        # only swap houses in this range
        houses_index = range(100, 148)

        # find a house to swap with
        for x in houses_index:
            swap_buddy = random.choice(houses_index)
            while x == swap_buddy:
                swap_buddy = random.choice(houses_index)

            # swap battery of two houses
            district.houses[x].swap_battery(district.houses[swap_buddy])

            # if battery capacity is exceeded swap back
            if district.houses[x].battery.total_input > district.houses[x].battery.capacity or district.houses[swap_buddy].battery.total_input > district.houses[swap_buddy].battery.capacity:
                # swap back
                district.houses[x].swap_battery(district.houses[swap_buddy])

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

                        # print(f'{self.total_connected_houses}')

    def remove_cable_connections(self, district):
        """remove all cable connections but keep in memory which house is connected to which battery"""

        for house in district.houses:
            house.cables = []

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

            # -- check to see if houses are sorted right --
            # print("print distance of house to battery: ", [house.distance_to_batt for house in battery.houses])

            # make list to keep track which houses are cable connected to a battery
            cable_connected_houses = []

            # loop over houses connected to that battery; start at nearest house
            for house in battery.houses:
                # connect closest house directly to battery
                if len(cable_connected_houses) == 0:
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
                                closest_distance = distance_house_cable
                                closest_cable = existing_cable

                    # add house to closest cable
                    house.add_cable_connection(closest_cable)
                    cable_connected_houses.append(house)
                    # print("Look for closest connection of house: ", house)
                    # print("Closest cable: ", closest_cable)
                    # print("Distance house to closest cable: ", closest_distance)

    def run(self):
        """ greedily assigns houses to the closest battery
        and swap houses until the capacity constraint is met"""

        total_costs = []

        for district in self.districts:
            # reset district first
            district.reset_costs()
            district.clear_connections()
            self.total_connected_houses = 0

            # connect houses to closest battery
            self.connect_closest_battery(district)

            # if not all connected, swap batteries of houses
            if self.total_connected_houses != 150:
                unconnected_houses = self.unconnected_houses(district)

                # keep swapping until all houses are connected
                while self.total_connected_houses != 150:
                    self.swap_houses(district, unconnected_houses)

            # if cables are shared
            if self.UNIQUE_CABLES == False:
                # remove duplicate cables on one grid segment
                district.remove_duplicate_cables()

                # remove all cable connections but keep in memory which house is connected to which battery
                self.remove_cable_connections(district)

                # create list of all houses connected per battery
                district.list_houses_per_battery()

                # add cables more efficiently
                self.add_efficient_cables(district)

                # add all cables into the district
                district.add_all_cables()

            # if cables are not shared
            elif self.UNIQUE_CABLES == True:
                # when all houses are connected AND constraints are met, add cable connections
                # print(f'{self.total_connected_houses}')
                for house in district.houses:
                    house.add_cable_connection(house.battery)

                # make list of connected houses per battery
                district.list_houses_per_battery()

                # add all cables in a district to one list
                district.add_all_cables()

            # calculate cost per district
            total_costs.append(district.calculate_total_costs())

        # return cost per district
        return total_costs
