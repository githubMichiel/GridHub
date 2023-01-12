import numpy as np
from battery import Battery
from house import House
import csv

class District:

    def __init__(self, id, is_unique):
        self.id = id
        self.batteries = []
        self.houses = []
        self.costs = 0

        # boolean: True if the cables are unique, False if cables can be shared
        self.is_unique = is_unique
        if self.is_unique:
            self.unique_cables = 'own-costs'
        else:
            self.unique_cables = 'shared-costs'

    def load_batteries(self, filename):
        """ load batteries into memory"""

        with open(filename, "r") as f:
            csvreader = csv.reader(f)

            # skip first line
            next(csvreader)

            for row in csvreader:
                x = row[0]
                y = row[1]
                capacity = row[2].strip()

                # create battery
                battery = Battery(x, y, capacity)
                self.batteries.append(battery)


    def load_houses(self, filename):
        """ load houses into memory"""

        with open(filename) as f:
            csvreader = csv.reader(f)

            # skip first line
            next(csvreader)

            for row in csvreader:
                x = row[0]
                y = row[1]
                max_output = row[2].strip()

                # create house
                house = House(x, y, max_output)
                self.houses.append(house)

    def __str__(self):
        return f'["district": {self.id},"{self.unique_cables}": {self.costs},]'
