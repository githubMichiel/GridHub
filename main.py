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

    ax.scatter([battery_1.x for battery_1 in districts[district].batteries], [battery_1.y for battery_1 in districts[district].batteries], s=80, c='r', marker="P", label='batteries')
    ax.scatter([house_1.x for house_1 in districts[district].houses],[house_1.y for house_1 in districts[district].houses], s=80, c='b', marker="p", label='houses')
    plt.xticks(np.arange(0, 51, step=1))
    plt.yticks(np.arange(0, 51, step=1))
    plt.grid(linestyle='--', linewidth=0.5)

    # manually plot cables
    x1 = np.array([38, 39, 39, 39])
    y1 = np.array([12, 12, 13, 14])
    plt.plot(x1, y1, c='black')


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

    # visualize each district
    plot_district(0)
    plot_district(1)
    plot_district(2)
    plt.show()

    # connect each house to a battery
    for district in districts:
        district.connect_house_battery()
        print(district.houses[0].battery.id)
        district.list_houses_battery()
