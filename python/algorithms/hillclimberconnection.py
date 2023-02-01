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
    by swapping house-battery connections """

    def __init__(self, districts):
        """ initialize hillclimber"""

        # raise exception if no valid solution
        for district in districts:
            if district.check_capacity_constraint() == False or district.all_houses_connected() == False:
                raise Exception("HillClimber requires a complete solution.")

        # keep track of best solution and their costs
        self.optimal_districts = copy.deepcopy(districts)

    def check_solution(self, district, i, new_costs):
        """ checks if the new solution is better"""

        # check for corresponding district
        if i == 0:
            old_costs = self.optimal_districts[0].costs
        elif i == 1:
            old_costs = self.optimal_districts[1].costs
        elif i == 2:
            old_costs = self.optimal_districts[2].costs

        # if solution is better
        if new_costs < old_costs:
            if i == 0:
                self.optimal_districts[0] = copy.deepcopy(district)
            elif i == 1:
                self.optimal_districts[1] = copy.deepcopy(district)
            elif i == 2:
                self.optimal_districts[2] = copy.deepcopy(district)

    def run(self, iterations):
        """ run hillclimber"""

        print("\n START HILLCLIMBER")

        # run iterations amount of times
        for iteration in range(iterations):
            # create copy of districts which can be altered
            new_district = copy.deepcopy(self.optimal_districts)

            # loop over districts
            for i in range(3):
                greedy = Greedy(new_district[i], UNIQUE_CABLES=False)
                costs = greedy.run(clear_cables_only=True, search_free_space=False, swap_index=2, swap_once=True, hillclimber=True)
                new_costs = copy.deepcopy(costs)

                # check if solution is better
                self.check_solution(new_district[i], i, new_costs)

        # return the best solution
        return self.optimal_districts
