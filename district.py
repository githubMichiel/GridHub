import numpy as np

class District:

    def __init__(self, id):
        self.id = id
        self.batteries = []
        self.houses = []

    def load_batteries(filename):
        """ load batteries into memory"""

        while True:
            with open(filename) as f:

                # read each line separately
                line = f.readline()

                # split line into components
                line = line.split(",")
                x = line[0]
                y = line[1]
                capacity = line[2]

                # create battery
                battery = Battery(x, y, capacity)
                self.batteries.append(battery)

            if line = "\n":
                break

    def load_houses(filename):
        """ load houses into memory"""

            while True:
                with open(filename) as f:

                    # read each line separately
                    line = f.readline()

                    # split line into components
                    line = line.split(",")
                    x = line[0]
                    y = line[1]
                    max_output = line[2]

                    # create battery
                    house = House(x, y, max_output)
                    self.houses.append(house)

                if line = "\n":
                    break

#    def __str__(self):

#        return f'[\n\{"district: "}]'
