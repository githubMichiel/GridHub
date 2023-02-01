import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np

from ..classes.district import District

def plot_district(district):
    """ create a visualization of a district"""

    fig = plt.figure()
    ax = fig.add_subplot()

    # plot batteries
    ax.scatter([battery.x for battery in district.batteries],
               [battery.y for battery in district.batteries],
               s=80, c='r', marker="P", label='batteries')

    # plot houses
    ax.scatter([house.x for house in district.houses],
               [house.y for house in district.houses],
               s=80, c='b', marker="p", label='houses')

    # plot each cable per house
    for house in district.houses:
        x = np.array([cable.start[0] for cable in house.cables])
        y = np.array([cable.start[1] for cable in house.cables])
        ax.plot(x, y, c='black', linewidth=0.5)

    # plot grid
    plt.xticks(ticks=np.arange(0, 51, step=1), labels='')
    plt.yticks(ticks=np.arange(0, 51, step=1), labels='')
    plt.grid(linestyle='--', linewidth=0.5)

    # plot title
    plt.title(f"District {district.id}")

    # create legend items
    cables = mlines.Line2D([], [], color='black',
                          markersize=15, label='cables')
    houses = mlines.Line2D([], [], color='blue', marker='p',
                          markersize=15, label='houses')
    batteries = mlines.Line2D([], [], color='red', marker='P',
                          markersize=15, label='batteries')

    # plot legend
    plt.legend(bbox_to_anchor=(0.75, 1.18), loc="upper left", handles=[cables, houses, batteries], framealpha=0.5)


def plot_distribution(configuration, all_costs, district):
    """create a visualization of the distribution of costs over multiple runs"""

    fig = plt.figure()

    # histogram of the data
    n, bins, patches = plt.hist(all_costs, 50, density=True, facecolor='g', alpha=0.75)

    # plot text around plot
    plt.xlabel('Costs')
    plt.ylabel('Frequency')
    plt.yticks(ticks=[])
    plt.grid()

    # plot title depending on configuration
    if configuration == 1:
        plt.title(f"Distribution of random solutions for district {district.id} (unique cables)")
    elif configuration == 2:
        plt.title(f"Distribution of greedy solutions for district {district.id} (unique cables)")
    elif configuration == 3:
        plt.title(f"Distribution of random solutions for district {district.id} (shared cables)")
    elif configuration == 4:
        plt.title(f"Distribution of greedy solutions for district {district.id} (shared cables)")
