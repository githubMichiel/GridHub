from ..classes.battery import Battery
from ..classes.house import House
from ..classes.cable import Cable
from ..classes.district import District
from ..algorithms.greedy import Greedy
import random
import copy

class HillClimberConnection:
    """ hill climber algorithm to search for optimal battery connection configuration
    by swapping battery connections """

    def __init__(self, districts):
        for district in districts:
            if district.check_capacity_constraint() == False or district.all_houses_connected() == False:
                raise Exception("HillClimber requires a complete solution.")
        self.districts_copy = copy.deepcopy(districts)
        self.total_costs_1 = self.districts_copy[0].calculate_total_costs()
        self.total_costs_2 = self.districts_copy[1].calculate_total_costs()
        self.total_costs_3 = self.districts_copy[2].calculate_total_costs()

    def check_solution(self, district, i):
        print(f"check solution of district {district.id}")
        district.costs = 0
        new_value = district.calculate_total_costs()
        if i == 0:
            old_value = self.total_costs_1
            print(f"old costs of district {district.id}: {self.total_costs_1}")

        if i == 1:
            old_value = self.total_costs_2
            print(f"old costs of district {district.id}: {self.total_costs_2}")

        if i == 2:
            old_value = self.total_costs_3
            print(f"old costs of district {district.id}: {self.total_costs_3}")

        print(f"new costs of district {district.id}: {new_value}")

        if new_value < old_value:
            print("BETER \n")
            if i == 0:
                self.total_costs_1 = new_value
                self.districts_OG[0] = district
            if i == 1:
                self.total_costs_2 = new_value
                self.districts_OG[1] = district
            if i == 2:
                self.total_costs_3 = new_value
                self.districts_OG[2] = district

    def run_greedy(self, greedy):

        district.reset_costs()

        # remove all cable connections but keep in memory which house is connected to which battery
        for house in district.houses:
            house.cables = []

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
        district.add_all_cables()
        district.calculate_total_costs()


    def run(self, iterations):
        print("\n START HILLCLIMBER")
        greedy = Greedy(self.districts_copy, UNIQUE_CABLES=False)

        for iteration in range(iterations):
            for i in range(3):
                # remove all cable connections within district
                self.districts_copy[i].clear_connections(cables_only=True)

                # swap house-battery connection with capacity constraint
                unconnected_houses = []
                succesful_swap = greedy.swap_houses(self.districts_copy[i], unconnected_houses, search_free_space=False, swap_index=2, swap_once=True)

                while succesful_swap is not True:
                    succesful_swap = greedy.swap_houses(self.districts_copy[i], unconnected_houses, search_free_space=False, swap_index=2, swap_once=True)
                    print("no succesful swap in hillclimber")

                # after succesful swap add cables with greedy algorithm
                # create list of all houses connected per battery
                self.districts_copy[i].list_houses_per_battery()

                # add cables more efficiently
                greedy.add_efficient_cables(self.districts_copy[i])

                # add all cables into the district
                self.districts_copy[i].add_all_cables()

                self.check_solution(self.districts_copy[i], i)


        return self.districts_copy
