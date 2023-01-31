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
        self.districts_OG = districts
        self.districts = copy.deepcopy(districts)
        self.total_costs_1 = self.districts[0].calculate_total_costs()
        self.total_costs_2 = self.districts[1].calculate_total_costs()
        self.total_costs_3 = self.districts[2].calculate_total_costs()

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

        else:
            print("SLECHTER\n")
            district.reset_costs()
            district.clear_connections(cables_only=True)


    def run(self, iterations):
        print("\n START HILLCLIMBER")
        greedy = Greedy(self.districts, UNIQUE_CABLES=False)

        for iteration in range(iterations):
            for i in range(3):
                # remove all cable connections within district
                self.districts[i].clear_connections(cables_only=True)

                # swap house-battery connection with capacity constraint
                unconnected_houses = []
                succesful_swap = greedy.swap_houses(self.districts[i], unconnected_houses, search_free_space=False, swap_index=2)

                while succesful_swap is not True:
                    succesful_swap = greedy.swap_houses(self.districts[i], unconnected_houses, search_free_space=False, swap_index=2)
                    print("no succesful swap in hillclimber")

                # after succesful swap add cables with greedy algorithm
                # create list of all houses connected per battery
                self.districts[i].list_houses_per_battery()

                # add cables more efficiently
                greedy.add_efficient_cables(self.districts[i])

                # add all cables into the district
                self.districts[i].add_all_cables()

                self.check_solution(self.districts[i], i)


        return self.districts_OG
