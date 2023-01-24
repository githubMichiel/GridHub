class HillClimber:

def __init__(self, district):
    if district.check_capacity_constraint() == False or district.all_houses_connected() == False:
        raise Exception("HillClimber requires a complete solution.")

    self.district = copy.deepcopy(district)
    self.value = district.calculate_total_costs()


def random_house(self):
    return random.choice(self.district.houses)

def replace_cable_connection(self, house):



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
