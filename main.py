"""
main.py

- Contains the main code used for solving the SmartGrid problem.
"""

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
import json
from sys import argv

from battery import Battery
from house import House
from district import District

# Global variables set based on the configuration
IS_RANDOM_ALGORITHM = False
IS_UNIQUE_CABLES = False
IS_VARIABLE_BATTERY_LOCATION = False
IS_MULTIPLE_BATTERY_TYPES = False

# run program until there are found NUMBER_OF_SOLUTIONS solutions
NUMBER_OF_SOLUTIONS = 1


def json_format(district):
    """create JSON format string that is needed at the end of the assignment"""

    district_info = repr(district)
    #TODO: find a way to do this for all batteries without hard coding it
    batteries = [repr(district.batteries[0]),repr(district.batteries[1]),repr(district.batteries[2]),repr(district.batteries[3]),repr(district.batteries[4])]
    return f'[{{{district_info}}}, {{{batteries[0]}}}, {{{batteries[1]}}}, {{{batteries[2]}}}, {{{batteries[3]}}}, {{{batteries[4]}}}]'

def json_output(string):
    """create JSON output that is needed at the end of the assignment"""

    parsed = json.loads(string)
    f = open("output.json", "w")
    f.write(json.dumps(parsed, indent=2))
    f.close()

def run_algorithm(districts):
    total_costs = []
    for district in districts:
        # reset district first
        district.reset_costs()
        district.clear_connections()

        # connect each house to a battery
        district.connect_house_battery(IS_RANDOM_ALGORITHM)
        for house in district.houses:
            if house.battery == None:
                print(f"House object has no battery")
            else:
                # when all houses are connected AND constraints are met, add cable connections
                house.add_connection(house.battery)

        # make list of connected houses per battery
        # CURRENTLY NOT USED
        #district.list_houses_battery()

        # make dictionary with batteries per district
        # CURRENTLY NOT USED
        #district.make_dict_district_batteries()

        # add all of the cables that are stored in all of the houses to the list of all cables of the district
        district.add_all_cables()

        # TODO: remove duplicates function doesnt work yet
        #district.remove_duplicate_cables()

        total_costs.append(district.calculate_total_costs())
    return total_costs

def run_multiple_simulations(districts):
    """run the program NUMBER_OF_SOLUTIONS times"""

    # store results per district
    results_1, results_2, results_3 = [], [], []
    results = [results_1, results_2, results_3]

    for i in range(0, NUMBER_OF_SOLUTIONS):
        print(f"Process: {i}")
        costs_single_run = run_algorithm(districts)
        results_1.append(costs_single_run[0])
        results_2.append(costs_single_run[1])
        results_3.append(costs_single_run[2])

    # print descriptive statistics per district
    for i in range(1, 4):
        print("")
        print(f"District {i}:")
        print(f"The lowest found cost: {min(results[i - 1])}")
        print(f"The highest found cost: {max(results[i - 1])}")

        mean = sum(results[i - 1]) / len(results[i - 1])
        print(f"The average found cost: {mean}")
        print("")
        print("")

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

    # plot each cable per house
    for house in districts[district].houses:
        x = np.array([cable.x for cable in house.cables])
        y = np.array([cable.y for cable in house.cables])
        ax.plot(x, y, c='black', linewidth=0.5)

    # plot grid
    plt.xticks(np.arange(0, 51, step=1))
    plt.yticks(np.arange(0, 51, step=1))
    plt.grid(linestyle='--', linewidth=0.5)

    # plot title
    plt.title(f"District {district + 1}")

    # create legend items
    cables = mlines.Line2D([], [], color='black',
                          markersize=15, label='cables')
    houses = mlines.Line2D([], [], color='blue', marker='p',
                          markersize=15, label='houses')
    batteries = mlines.Line2D([], [], color='red', marker='P',
                          markersize=15, label='batteries')
    # mogelijk nog de totale kosten berekenen en ook in de legenda plaatsen

    # plot legend
    plt.legend(bbox_to_anchor=(0.75, 1.18), loc="upper left", handles=[cables, houses, batteries], framealpha=0.5)


if __name__ == "__main__":

    # check command line arguments
    if len(argv) != 2 or int(argv[1]) not in range(1,6):
        print("Usage: python main.py [int]")
        print("Choose 1 for random algorithm with unique cables.")
        print("Choose 2 for greedy algorithm with unique cables.")
        print("Choose 3 for random algorithm with shared cables")
        print("Choose 4 for greedy algorithm with shared cables")
        print("Choose 5 for greedy algorithm with variable batteries and shared cables")
        print("Choose 6 for greedy algorithm with different variable batteries and shared cables")
        exit(1)

    configuration = int(argv[1])

    if configuration == 1 or configuration == 3:
        IS_RANDOM_ALGORITHM = True

    if configuration == 1 or configuration == 2:
        IS_UNIQUE_CABLES = True

    if configuration == 5 or configuration == 6:
        IS_VARIABLE_BATTERY_LOCATION = True
        if configuration == 6:
            IS_MULTIPLE_BATTERY_TYPES = True

    # create districts
    districts = []
    for i in range(1,4):
        districts.append(District(i, IS_UNIQUE_CABLES))

    # load objects into districts
    districts[0].load_houses('district-1_houses.csv')
    districts[0].load_batteries('district-1_batteries.csv')
    districts[1].load_houses('district-2_houses.csv')
    districts[1].load_batteries('district-2_batteries.csv')
    districts[2].load_houses('district-3_houses.csv')
    districts[2].load_batteries('district-3_batteries.csv')

    # run corresponding algorithm
    if IS_RANDOM_ALGORITHM:
        run_multiple_simulations(districts)
    else:
        run_algorithm(districts)

    # visualise each district
    plot_district(0)
    plot_district(1)
    plot_district(2)
    plt.show()
