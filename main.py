"""
smartgrid.py

-
"""

from battery import Battery
from house import House
from district import District


class District:

    def __init__(self):
        self.batteries = []
        self.houses = []

#    def __str__(self):

#        return f'[\n\{"district: "}]'

    def load_batteries(filename):
        """ load batteries into memory"""

        while True:
            with open(filename) as f:

<<<<<<< HEAD
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


if __name__ == "__main__":

    # create district
    district = District()
=======
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

if __name__ == "__main__":
    districts = []
    for i in range(1,4):
        districts.append(District(i))
        #TODO: adding the houses and batteries to the districts
>>>>>>> 67e7ecd8f89ed0295c0152b9bf2c718e2ee0f6df
