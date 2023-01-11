import numpy as np
from battery import Battery
from house import House

class District:

    def __init__(self, id):
        self.id = id
        self.batteries = []
        self.houses = []

    def load_batteries(self, filename):
        """ load batteries into memory"""

        with open(filename) as f:
            while True:
                # read each line separately
                line = f.readline()

                # split line into components
                line = line.split(",")
                x = line[0]
                y = line[1]
                capacity = line[2].strip()

                # create battery
                battery = Battery(x, y, capacity)
                self.batteries.append(battery)

                if line == "\n":
                    break

    def load_houses(self, filename):
        """ load houses into memory"""

        with open(filename) as f:
            while True:
                # read each line separately
                line = f.readline()[1:]

                # split line into components
                line = line.split(",")
                print(line)
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
