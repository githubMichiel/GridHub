import numpy as np
from battery import Battery
from house import House
import csv

class District:

    def __init__(self, id):
        self.id = id
        self.batteries = []
        self.houses = []

    def load_batteries(self, filename):
        """ load batteries into memory"""

        with open(filename, "r") as f:

            csvreader = csv.reader(f)
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
            next(csvreader)

            for row in csvreader:
                # read each line separately
                line = f.readline()

                # split line into components
                line = line.split(",")
                x = line[0]
                y = line[1]
                max_output = line[2].strip()

                # create house
                house = House(x, y, max_output)
                self.houses.append(house)

                if line == "\n":
                    break
#    def __str__(self):

#        return f'[\n\{"district: "}]'
