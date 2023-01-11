import numpy as np

class District:

    def __init__(self):

    def __init__(self, id):
        self.id = id
        self.batteries = []
        self.houses = []


    def add_house(self, house):
        self.houses.append(house)

    def add_battery(self, battery):
        self.batteries.append(battery)

#    def __str__(self):

#        return f'[\n\{"district: "}]'
