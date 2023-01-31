import random
import copy
from .greedy import Greedy

class HillClimber:

    def __init__(self, districts):
        for district in districts:
            if district.check_capacity_constraint() == False or district.all_houses_connected() == False:
                raise Exception("HillClimber requires a complete solution.")

        self.districts = districts
        self.number_of_districts = len(self.districts)
        self.values = []
        for district in self.districts:
            self.values.append(district.calculate_total_costs())

    def random_battery(self, district):
        return random.choice(district.batteries)

    def possible_directions(self, battery):
        all_directions = [(1,0), (0,1), (-1,0), (0,-1)]
        valid_direction = [1, 1, 1, 1]
        possible_directions = []
        for house in self.districts[0].houses:
            for i in range(4):
                if battery.x + all_directions[i][0] == house.x and battery.y + all_directions[i][1] == house.y:
                    valid_direction[i] = 0
        for other_battery in self.districts[0].batteries:
            for i in range(4):
                if battery.x + all_directions[i][0] == house.x and battery.y + all_directions[i][1] == house.y:
                    valid_direction[i] = 0
        for i in range(4):
            if valid_direction[i] == 1:
                possible_directions.append(all_directions[i])

        if len(possible_directions) != 0:
            return possible_directions
        else:
            return [(0,0)]

    def change_battery_location(self, battery):
        random_direction = random.choice(self.possible_directions(battery))
        battery.x += random_direction[0]
        battery.y += random_direction[1]
        return random_direction

    def change_battery_location_back(self, battery, direction):
        battery.x -= direction[0]
        battery.y -= direction[1]

    def run_greedy(self):
        #greedy = Greedy(self.districts, False)
        for district in self.districts:

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
                random_direction = self.change_battery_location(random_battery)
                random_batteries.append(random_battery)
                random_directions.append(random_direction)
            self.run_greedy()
            self.check_solution(random_batteries, random_directions)
