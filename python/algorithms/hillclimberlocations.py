import random
import copy
from .greedy import Greedy

class HillClimberLocations:
    """ hill climber algorithm that moves the batteries around to find a better solution"""

    def __init__(self, districts):
        """ initialize hill climber"""

        # raise exception if no valid solution
        for district in districts:
            if district.check_capacity_constraint() == False or district.all_houses_connected() == False:
                raise Exception("HillClimber requires a complete solution.")

        # start with a district and its costs
        self.districts = districts
        self.optimal_costs = []

        for district in self.districts:
            self.optimal_costs.append(district.calculate_total_costs())

    def random_battery(self, district):
        """ chooses a random battery to move around"""

        return random.choice(district.batteries)

    def possible_directions(self, battery, district_index):
        """ determine which direction the battery could go
        cannot move onto a location with another house or battery"""

        # possible directions
        all_directions = [(1,0), (0,1), (-1,0), (0,-1)]
        valid_direction = [1, 1, 1, 1]
        possible_directions = []

        # loop over houses in a district
        for house in self.districts[district_index].houses:
            for i in range(4):
                # there is a house in this direction
                if battery.x + all_directions[i][0] == house.x and battery.y + all_directions[i][1] == house.y:
                    # remove direction from valid directions
                    valid_direction[i] = 0
        # loop over batteries in a district
        for other_battery in self.districts[district_index].batteries:
            for i in range(4):
                # there is a battery in this direction
                if battery.x + all_directions[i][0] == other_battery.x and battery.y + all_directions[i][1] == other_battery.y:
                    # remove direction from valid directions
                    valid_direction[i] = 0
        for i in range(4):
            # if direction is valid
            if valid_direction[i] == 1:
                # add direction to possible directions
                possible_directions.append(all_directions[i])

        # if there are valid directions
        if len(possible_directions) != 0:
            return possible_directions
        # if no valid direction
        else:
            return [(0,0)]

    def change_battery_location(self, battery, district_index):
        """ changes the location of a battery with as step of size 1"""

        # choose a random direction of the possibilities
        random_direction = random.choice(self.possible_directions(battery, district_index))

        # change coordinates
        battery.x += random_direction[0]
        battery.y += random_direction[1]

        # return the direction the battery went
        return random_direction

    def change_battery_location_back(self, battery, direction):
        """ changes the location of a battery back if the new solution is worse"""

        battery.x -= direction[0]
        battery.y -= direction[1]

    def run_greedy(self):
        """ greedy algorithm should be run before running the hillclimber"""

        # initialise greedy object
        greedy = Greedy(self.districts, False)

        # loop over districts
        for district in self.districts:
            # reset district first
            district.reset_costs()

            # remove all cable connections but keep in memory which house is connected to which battery
            greedy.remove_cable_connections(district)

            # create list of all houses connected per battery
            district.list_houses_per_battery()

            # add cables more efficiently
            greedy.add_efficient_cables(district)

            # add all cables into the district
            district.add_all_cables()
            district.calculate_total_costs()

    def check_solution(self, batteries, directions):
        """ determines if the new solution is an improvement or not"""

        # loop over the list of costs
        for i in range(3):
            # determine new and old costs
            new_value = self.districts[i].costs
            old_value = self.optimal_costs[i]

            # replace cost if solution is better
            if new_value <= old_value:
                self.optimal_costs[i] = new_value
            # undo battery step if solution is worse
            else:
                self.change_battery_location_back(batteries[i], directions[i])

    def run(self, iterations):
        """ run the hillclimber"""

        print(' \n START HILLCLIMBER')

        # run iteration times
        for iteration in range(iterations):
            # initialize variables
            random_batteries = []
            random_directions = []

            # loop over districts
            for i in range(3):
                # choose random battery and direction
                random_battery = self.random_battery(self.districts[i])
                random_direction = self.change_battery_location(random_battery, i)
                random_batteries.append(random_battery)
                random_directions.append(random_direction)

            next_districts = self.run_greedy()

            # check if the new solution is better
            self.check_solution(random_batteries, random_directions)

        # return the districts
        return self.districts
