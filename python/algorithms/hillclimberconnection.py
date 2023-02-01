from ..classes.battery import Battery
from ..classes.house import House
from ..classes.cable import Cable
from ..classes.district import District
from ..algorithms.greedy import Greedy
from ..visualizations.visualize import plot_district
import random
import copy

class HillClimberConnection:
    """ hill climber algorithm to search for optimal battery connection configuration
    by swapping battery connections """

    def __init__(self, districts):
        for district in districts:
            if district.check_capacity_constraint() == False or district.all_houses_connected() == False:
                raise Exception("HillClimber requires a complete solution.")
        self.optimal_districts = copy.deepcopy(districts)
        self.optimal_cost_1 = copy.deepcopy(districts[0].costs)
        self.optimal_cost_2 = copy.deepcopy(districts[1].costs)
        self.optimal_cost_3 = copy.deepcopy(districts[2].costs)

    def check_solution(self, district, i, new_costs):
        print(f"check solution of district {district.id}")
        # district.costs = 0
        if i == 0:
            old_value = self.optimal_cost_1
            print(f"old costs of district {district.id}: {old_value}")

        if i == 1:
            old_value = self.optimal_cost_2
            print(f"old costs of district {district.id}: {old_value}")

        if i == 2:
            old_value = self.optimal_cost_3
            print(f"old costs of district {district.id}: {old_value}")

        print(f"new costs of district {district.id}: {new_costs}")

        if new_costs < old_value:
            print("BETER \n")
            if i == 0:
                self.optimal_cost_1 = new_costs
                self.optimal_districts[0] = district
            if i == 1:
                self.optimal_cost_1 = new_costs
                self.optimal_districts[1] = district
            if i == 2:
                self.optimal_cost_1 = new_costs
                self.optimal_districts[2] = district

    def run(self, iterations):
        print("\n START HILLCLIMBER")
        for iteration in range(iterations):
            district_experiment = copy.deepcopy(self.optimal_districts)
            for i in range(3):
                greedy = Greedy(district_experiment[i], UNIQUE_CABLES=False)
                new_costs = greedy.run(clear_cables_only=True, search_free_space=False, swap_index=2, swap_once=True, hillclimber=True)

                print(f"\n print cables of district {i}: {len(district_experiment[i].all_cables)}")
                # plot_district(district_experiment[i])
                self.check_solution(district_experiment[i], i, new_costs)


        return self.optimal_districts
