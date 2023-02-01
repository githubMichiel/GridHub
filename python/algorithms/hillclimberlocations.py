import random
import copy
from .greedy import Greedy

class HillClimberLocations:

    def __init__(self, districts):
        for district in districts:
            if district.check_capacity_constraint() == False or district.all_houses_connected() == False:
                raise Exception("HillClimber requires a complete solution.")

        self.districts = districts
        self.values = []
        for district in self.districts:
            self.values.append(district.calculate_total_costs())

    def random_battery(self, district):
        return random.choice(district.batteries)

    def possible_directions(self, battery, district_index):
        all_directions = [(1,0), (0,1), (-1,0), (0,-1)]
        valid_direction = [1, 1, 1, 1]
        possible_directions = []
        for house in self.districts[district_index].houses:
            for i in range(4):
                if battery.x + all_directions[i][0] == house.x and battery.y + all_directions[i][1] == house.y:
                    valid_direction[i] = 0
        for other_battery in self.districts[district_index].batteries:
            for i in range(4):
                if battery.x + all_directions[i][0] == other_battery.x and battery.y + all_directions[i][1] == other_battery.y:
                    valid_direction[i] = 0
        for i in range(4):
            if valid_direction[i] == 1:
                possible_directions.append(all_directions[i])

        if len(possible_directions) != 0:
            return possible_directions
        else:
            return [(0,0)]

    def change_battery_location(self, battery, district_index):
        random_direction = random.choice(self.possible_directions(battery, district_index))
        battery.x += random_direction[0]
        battery.y += random_direction[1]
        return random_direction

    def change_battery_location_back(self, battery, direction):
        battery.x -= direction[0]
        battery.y -= direction[1]

    def run_greedy(self):
        greedy = Greedy(self.districts, False)

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
        for i in range(3):
            new_value = self.districts[i].costs
            old_value = self.values[i]

            if new_value <= old_value:
                self.values[i] = new_value
            else:
                self.change_battery_location_back(batteries[i], directions[i])


    def run(self, iterations):
        for iteration in range(iterations):
            random_batteries = []
            random_directions = []
            for i in range(3):
                random_battery = self.random_battery(self.districts[i])
                random_direction = self.change_battery_location(random_battery, i)
                random_batteries.append(random_battery)
                random_directions.append(random_direction)
            self.run_greedy()
            self.check_solution(random_batteries, random_directions)
        return self.districts
