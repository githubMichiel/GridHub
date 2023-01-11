"""
smartgrid.py

-
"""

from battery import Battery
from house import House
from district import District

def load_batteries(filename):
    """ load the batteries into memory"""

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


def load_houses(filename):
    """ load houses into memory"""

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
