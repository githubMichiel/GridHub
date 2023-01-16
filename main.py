"""
smartgrid.py

-
"""

import matplotlib.pyplot as plt
import numpy as np
import json

from battery import Battery
from house import House
from district import District

#def json_format(district):
#    district_info = repr(district)
    #TODO: find a way to do this for all batteries without hard coding it
#    batteries = [repr(district.batteries[0]),repr(district.batteries[1]),repr(district.batteries[2]),repr(district.batteries[3]),repr(district.batteries[4])]
#    return f'[{{{district_info}}}, {{{batteries[0]}}}, {{{batteries[1]}}}, {{{batteries[2]}}}, {{{batteries[3]}}}, {{{batteries[4]}}}]'

#def json_output(string):
    #parsed = json.loads(string)
    #print(json.dumps(parsed,indent=2))

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
        x = np.array([x[0] for x in house.cables])
        y = np.array([x[1] for x in house.cables])
        plt.plot(x, y, c='black', linewidth=0.5)


if __name__ == "__main__":

    # create districts
    districts = []
    for i in range(1,4):
        districts.append(District(i, True))

    # load objects into districts
    districts[0].load_houses('district-1_houses.csv')
    districts[0].load_batteries('district-1_batteries.csv')
    districts[1].load_houses('district-2_houses.csv')
    districts[1].load_batteries('district-2_batteries.csv')
    districts[2].load_houses('district-3_houses.csv')
    districts[2].load_batteries('district-3_batteries.csv')

    #test = json_format(districts[0])
    #json_output(test)

    # apply functions to each district
    for district in districts:
        # connect each house to a battery
        district.connect_house_battery()

        # make list of connected houses per battery
        district.list_houses_battery()

        # make dictionary with batteries per district
        district.make_dict_district_batteries()

        # test the total cost functions
        district.add_all_cables()
        district.remove_duplicate_cables()
        district.total_costs()
        print(district.costs)

    # visualize each district
    plot_district(0)
    plot_district(1)
    plot_district(2)
    plt.show()
