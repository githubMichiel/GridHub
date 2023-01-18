"""
smartgrid.py

-
"""

import matplotlib.pyplot as plt
import numpy as np
import json
from sys import argv

from battery import Battery
from house import House
from district import District

def json_format(district):
    district_info = repr(district)
    #TODO: find a way to do this for all batteries without hard coding it
    batteries = [repr(district.batteries[0]),repr(district.batteries[1]),repr(district.batteries[2]),repr(district.batteries[3]),repr(district.batteries[4])]
    return f'[{{{district_info}}}, {{{batteries[0]}}}, {{{batteries[1]}}}, {{{batteries[2]}}}, {{{batteries[3]}}}, {{{batteries[4]}}}]'

def json_output(string):
    parsed = json.loads(string)
    f = open("output.json", "w")
    f.write(json.dumps(parsed, indent=2))
    f.close()

def plot_district(district):
    """ create a visualization of a district"""

    fig = plt.figure()
    ax = fig.add_subplot()

    # plot batteries
    ax.scatter([battery.x for battery in districts[district].batteries],
               [battery.y for battery in districts[district].batteries],
               s=80, c='r', marker="P", label='batteries')

    # plot houses
    ax.scatter([house.x for house in districts[district].houses],
               [house.y for house in districts[district].houses],
               s=80, c='b', marker="p", label='houses')

    # plot grid
    plt.xticks(np.arange(0, 51, step=1))
    plt.yticks(np.arange(0, 51, step=1))
    plt.grid(linestyle='--', linewidth=0.5)

    # plot each cable per house
    for house in districts[district].houses:
        x = np.array([cable.x for cable in house.cables])
        y = np.array([cable.y for cable in house.cables])
        plt.plot(x, y, c='black', linewidth=0.5)


if __name__ == "__main__":

    # check command line arguments
    if len(argv) != 2:
        print("Usage: python main.py [int]")
        print("Choose 1 for random algorithm.")
        print("Choose 2 for greedy algorithm.")
        exit(1)

    # store the chosen algorithm
    algorithm = argv[1]

    # create districts
    districts = []
    for i in range(1,4):
        districts.append(District(i, False))

    # load objects into districts
    districts[0].load_houses('district-1_houses.csv')
    districts[0].load_batteries('district-1_batteries.csv')
    districts[1].load_houses('district-2_houses.csv')
    districts[1].load_batteries('district-2_batteries.csv')
    districts[2].load_houses('district-3_houses.csv')
    districts[2].load_batteries('district-3_batteries.csv')


    # apply functions to each district
    for district in districts:
        # connect each house to a battery

        # 1: randomly
        # 2: greedy
        district.connect_house_battery(algorithm)
        for house in district.houses:
            if house.battery == None:
                print(f"House object has no battery: {house.battery}")
            else:
                # when all houses are connected AND constraints are met, add cable connections
                house.add_connection(house.battery)


        # make list of connected houses per battery
        district.list_houses_battery()

        # make dictionary with batteries per district
        district.make_dict_district_batteries()

        # add all of the cables that are stored in all of the houses to the list of all cables of the district
        district.add_all_cables()

        # TODO: remove duplicates function doesnt work yet
        #district.remove_duplicate_cables()

        district.total_costs()
        print(f"Total costs of district: {district.costs}")

        for battery in district.batteries:
            battery.print_input()


    # visualize each district
    plot_district(0)
    plot_district(1)
    plot_district(2)
    plt.show()
