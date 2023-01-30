from .battery import Battery
from .house import House
from .cable import Cable
from .district import District
import random
import copy


class HillClimber:

    def __init__(self, district):
        if district.check_capacity_constraint() == False or district.all_houses_connected() == False:
            raise Exception("HillClimber requires a complete solution.")

        self.district = copy.deepcopy(district)
        self.value = district.calculate_total_costs()
        self.unconnected_houses = []
        self.connected_houses = []

    def random_house(self):
        return random.choice(self.district.houses)

    def list_unconnected_and_connected_houses(self,house):
        unconnected_houses = []
        connected_houses = []
        for other_house in house.battery.houses:
            if other_house != house:
                if self.is_connected(other_house):
                    connected_houses.append(other_house)
                else:
                    unconnected_houses.append(other_house)
        self.unconnected_houses = unconnected_houses
        self.connected_houses = connected_houses

    def replace_cable_connection(self, house):

        # if at the end the closest cable is the same as it is now then we removed and added the same connection so we never need to store a previous state
        # closest cable piece is the last cable piece in a house its cable list because thats the way its currently connected to the battery
        if house.cables[-1].end == (house.battery.x, house.battery.y):
            return
        #shortest distance is the existing cable connection length
        closest_distance = len(house.cables)
        previous_cables = copy.deepcopy(house.cables)
        #clear the current cable connection
        house.cables = []

        best_total_costs = self.value

        # each cable connection between 1 battery and all of the houses its connected to
        for next_cable_connection in house.battery.houses:
            # each cable piece of a given cable connection
            for next_cable in next_cable_connection.cables:
                next_distance = self.district.calculate_distance(house, next_cable)
                if next_distance < closest_distance:
                    house.add_connection(next_cable)
                    self.list_unconnected_and_connected_houses(house)
                    previous_state_unconnected_houses = self.connect_unconnected_houses()
                    self.district.reset_costs()
                    self.district.add_all_cables()
                    new_total_costs = self.district.calculate_total_costs()
                    if new_total_costs < best_total_costs:
                        return
                    house.cables = []
                    self.restore_previous_state(previous_state_unconnected_houses)
        house.cables = previous_cables

    def connect_unconnected_houses(self):
        closest_distance = 101
        previous_state_unconnected_houses = []
        for unconnected_house in self.unconnected_houses:
            previous_state_unconnected_houses.append(copy.deepcopy(unconnected_house.cables))
            unconnected_house.cables = []
            for connected_house in self.connected_houses:
                for existing_cable in connected_house.cables:
                    next_distance = self.district.calculate_distance(unconnected_house, existing_cable)
                    if next_distance < closest_distance:
                        closest_distance = next_distance
                        closest_cable = existing_cable

            # add house to closest cable
            unconnected_house.add_connection(closest_cable)
            self.connected_houses.append(unconnected_house)
        return previous_state_unconnected_houses

    def is_connected(self, house):
        if len(house.cables) == 0:
            return False
        for other_house in house.battery.houses:
            if other_house != house:
                for cable in other_house.cables:
                    if house.cables[-1].end == cable.end or house.cables[-1].end == cable.start or house.cables[-1].end == (house.battery.x, house.battery.y):
                        return True
        return False

    def restore_previous_state(self, previous_state_unconnected_houses):
        index = 0
        for unconnected_house in self.unconnected_houses:
            unconnected_house.cables = copy.deepcopy(previous_state_unconnected_houses[index])
            index += 1

    def check_solution(self):
        self.district.reset_costs()
        self.district.add_all_cables()
        new_value = self.district.calculate_total_costs()
        old_value = self.value

        if new_value <= old_value:
            self.value = new_value

    def run(self, iterations):
        for iteration in range(iterations):
            self.replace_cable_connection(self.random_house())
            self.check_solution()
