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

def json_output():
    return

if __name__ == "__main__":

    # create districts
    districts = []
    for i in range(1,4):
        districts.append(District(i, True))
    districts[0].load_houses('district-1_houses.csv')
    districts[0].load_batteries('district-1_batteries.csv')
    districts[1].load_houses('district-2_houses.csv')
    districts[1].load_batteries('district-2_batteries.csv')
    districts[2].load_houses('district-3_houses.csv')
    districts[2].load_batteries('district-3_batteries.csv')

    #print(district[0].houses)
    #print(district[0].batteries)
    #print(json_output())
    #parsed = json.loads(json_output())
    #print(json.dumps(parsed, indent=4))

    # lists with x, y coordinates per district
    battery_1_x = []
    battery_1_y = []
    house_1_x = []
    house_1_y = []
    battery_2_x = []
    battery_2_y = []
    house_2_x = []
    house_2_y = []
    battery_3_x = []
    battery_3_y = []
    house_3_x = []
    house_3_y = []

    # retrieve battery coordinates separately for plotting
    for i in range(len(districts[0].batteries)):
        battery_1_x.append(int(districts[0].batteries[i].x))
        battery_1_y.append(int(districts[0].batteries[i].y))
        battery_2_x.append(int(districts[1].batteries[i].x))
        battery_2_y.append(int(districts[1].batteries[i].y))
        battery_3_x.append(int(districts[2].batteries[i].x))
        battery_3_y.append(int(districts[2].batteries[i].y))

    # retrieve house coordinates separately for plotting
    for i in range(len(districts[0].houses)):
        house_1_x.append(int(districts[0].houses[i].x))
        house_1_y.append(int(districts[0].houses[i].y))
        house_2_x.append(int(districts[1].houses[i].x))
        house_2_y.append(int(districts[1].houses[i].y))
        house_3_x.append(int(districts[2].houses[i].x))
        house_3_y.append(int(districts[2].houses[i].y))


    # figure district 1
    fig1 = plt.figure()
    ax1 = fig1.add_subplot()

    ax1.scatter(battery_1_x, battery_1_y, s=80, c='r', marker="P", label='first')
    ax1.scatter(house_1_x, house_1_y, s=80, c='b', marker="p", label='second')
    plt.xticks(np.arange(0, 51, step=1))
    plt.yticks(np.arange(0, 51, step=1))
    plt.grid(linestyle='--', linewidth=0.5)

    x1 = np.array([38, 39, 39, 39])
    y1 = np.array([12, 12, 13, 14])
    plt.plot(x1, y1, c='black')

    # figure district 2
    fig2 = plt.figure()
    ax2 = fig2.add_subplot()

    ax2.scatter(battery_2_x, battery_2_y, s=80, c='r', marker="P", label='first')
    ax2.scatter(house_2_x, house_2_y, s=80, c='b', marker="p", label='second')
    plt.xticks(np.arange(0, 51, step=1))
    plt.yticks(np.arange(0, 51, step=1))
    plt.grid(linestyle='--', linewidth=0.5)

    # figure district 3
    fig3 = plt.figure()
    ax3 = fig3.add_subplot()

    ax3.scatter(battery_3_x, battery_3_y, s=80, c='r', marker="P", label='first')
    ax3.scatter(house_3_x, house_3_y, s=80, c='b', marker="p", label='second')
    plt.xticks(np.arange(0, 51, step=1))
    plt.yticks(np.arange(0, 51, step=1))
    plt.grid(linestyle='--', linewidth=0.5)

    plt.show()
