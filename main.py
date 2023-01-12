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

    # figure district 1
    fig1 = plt.figure()
    ax1 = fig1.add_subplot()

    ax1.scatter([battery_1.x for battery_1 in districts[0].batteries], [battery_1.y for battery_1 in districts[0].batteries], s=80, c='r', marker="P", label='first')
    ax1.scatter([house_1.x for house_1 in districts[0].houses],[house_1.y for house_1 in districts[0].houses], s=80, c='b', marker="p", label='second')
    plt.xticks(np.arange(0, 51, step=1))
    plt.yticks(np.arange(0, 51, step=1))
    plt.grid(linestyle='--', linewidth=0.5)

    # manually plot cables
    x1 = np.array([38, 39, 39, 39])
    y1 = np.array([12, 12, 13, 14])
    plt.plot(x1, y1, c='black')

    # figure district 2
    fig2 = plt.figure()
    ax2 = fig2.add_subplot()

    ax2.scatter([battery_2.x for battery_2 in districts[1].batteries], [battery_2.y for battery_2 in districts[1].batteries], s=80, c='r', marker="P", label='first')
    ax2.scatter([house_2.x for house_2 in districts[1].houses], [house_2.y for house_2 in districts[1].houses], s=80, c='b', marker="p", label='second')
    plt.xticks(np.arange(0, 51, step=1))
    plt.yticks(np.arange(0, 51, step=1))
    plt.grid(linestyle='--', linewidth=0.5)

    # figure district 3
    fig3 = plt.figure()
    ax3 = fig3.add_subplot()

    ax3.scatter([battery_3.x for battery_3 in districts[2].batteries], [battery_3.y for battery_3 in districts[2].batteries], s=80, c='r', marker="P", label='first')
    ax3.scatter([house_3.x for house_3 in districts[2].houses], [house_3.y for house_3 in districts[2].houses], s=80, c='b', marker="p", label='second')
    plt.xticks(np.arange(0, 51, step=1))
    plt.yticks(np.arange(0, 51, step=1))
    plt.grid(linestyle='--', linewidth=0.5)

    plt.show()

    # connect houses to 1_batteries
    districts[0].connect_house_battery()
    print(districts[0].houses[0].battery.id)
