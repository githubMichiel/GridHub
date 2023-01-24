from .battery import Battery
from .house import House
from .cable import Cable
from .district import District

class HillClimber:

def __init__(self, district):
    if district.check_capacity_constraint() == False or district.all_houses_connected() == False:
        raise Exception("HillClimber requires a complete solution.")

    self.district = copy.deepcopy(district)
    self.value = district.calculate_total_costs()


def random_house(self):
    return random.choice(self.district.houses)

def replace_cable_connection(self, house):
    closest_cable = None
    closest_distance = 101
    for next_cable in self.district.all_cables:

        next_distance = self.district.calculate_distance(house, next_cable)
        if next_distance <= closest_distance:
            closest_distance = next_distance
            closest_cable = next_cable


def check_solution(self, new_district):
    new_value = new_district.calculate_total_costs()
    old_value = self.value

    if new_value <= old_value:
        self.district = new_district
        self.value = new_value

def run(self, iterations):
    for iteration in range(iterations):
        new_district = copy.deepcopy(district)
        self.replace_cable_connection(self.random_house())
        self.check_solution(new_district)
