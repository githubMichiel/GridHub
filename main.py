"""
main.py

- Contains the main code used for solving the SmartGrid problem.
"""
import matplotlib.pyplot as plt
import numpy as np
import json
from sys import argv

from python.algorithms import randomise as rd
from python.algorithms import greedy

from python.classes.district import District
from python.classes.battery import Battery
from python.classes.house import House
from python.classes.cable import Cable
from python.visualizations.visualize import plot_district

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

def run_multiple_simulations(districts):
    """run the program NUMBER_OF_SOLUTIONS times"""

    # store results per district
    results_1, results_2, results_3 = [], [], []
    results = [results_1, results_2, results_3]

    for i in range(0, NUMBER_OF_SOLUTIONS):
        print(f"Process: {i}")

        # run corresponding algorithm
        if IS_RANDOM_ALGORITHM:
            costs_single_run = random_algorithm(districts)
        else:
            costs_single_run = greedy_algorithm(districts)

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


if __name__ == "__main__":

    # check command line arguments
    if len(argv) != 2 or int(argv[1]) not in range(1,7):
        print("Usage: python main.py [int]")
        print("Choose 1 for random algorithm with unique cables.")
        print("Choose 2 for greedy algorithm with unique cables.")
        print("Choose 3 for random algorithm with shared cables")
        print("Choose 4 for greedy algorithm with shared cables")
        print("Choose 5 for greedy algorithm with variable batteries and shared cables")
        print("Choose 6 for greedy algorithm with different variable batteries and shared cables")
        exit(1)

    # determine how the program should be run
    configuration = int(argv[1])

    # determine if random algorithm is used
    if configuration == 1 or configuration == 3:
        IS_RANDOM_ALGORITHM = True

    # determine if cables are shared or unique
    if configuration == 1 or configuration == 2:
        IS_UNIQUE_CABLES = True

    # determine how batteries should be implemented
    if configuration == 5 or configuration == 6:
        IS_VARIABLE_BATTERY_LOCATION = True
        if configuration == 6:
            IS_MULTIPLE_BATTERY_TYPES = True

    # create districts
    districts = []
    for i in range(1,4):
        districts.append(District(i, IS_UNIQUE_CABLES))

    # load objects into districts
    districts[0].load_houses('data/district-1_houses.csv')
    districts[0].load_batteries('data/district-1_batteries.csv')
    districts[1].load_houses('data/district-2_houses.csv')
    districts[1].load_batteries('data/district-2_batteries.csv')
    districts[2].load_houses('data/district-3_houses.csv')
    districts[2].load_batteries('data/district-3_batteries.csv')

    # run algorithm based on configuration
    # random + unique cables
    if configuration == 1:
        print('Implementing random algorithm with unique cables...')
        costs = rd.random_algorithm(districts, IS_UNIQUE_CABLES)
        print(f'Cost per district: {costs}')

    # greedy + unique cables
    elif configuration == 2:
        print('Implementing greedy algorithm with unique cables...')
        costs = greedy.greedy_algorithm(districts, IS_UNIQUE_CABLES)
        print(f'Cost per district: {costs}')

    # random + shared cables
    elif configuration == 3:
        print('Implementing random algorithm with shared cables...')
        costs = rd.random_algorithm(districts, IS_UNIQUE_CABLES)
        print(f'Cost per district: {costs}')

    # greedy + shared cables
    elif configuration == 4:
        print('Implementing greedy algorithm with shared cables...')
        costs = greedy.greedy_algorithm(districts, IS_UNIQUE_CABLES)
        print(f'Cost per district: {costs}')

    # greedy + shared cables + variable battery location
    elif configuration == 5:
        print('Implementing greedy algorithm with shared cables.')
        print('Finding optimal coordinates for each battery...')
        pass

    # greedy + shared cables + variable battery location + different batteries
    elif configuration == 6:
        print('Implementing greedy algorithm with shared cables.')
        print('Finding optimal configuration with different batteries...')
        pass

    # visualise each district
    plot_district(districts[0])
    plot_district(districts[1])
    plot_district(districts[2])
    plt.show()

    # create JSON output
    json_output(json_format(districts[0]))

    #
    print(f"total amount of cables in district 1: {len(districts[0].all_cables)}")
    print(f"total amount of cables in district 2: {len(districts[1].all_cables)}")
    print(f"total amount of cables in district 3: {len(districts[2].all_cables)}")
