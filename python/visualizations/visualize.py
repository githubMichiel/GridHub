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
        x = np.array([cable.x for cable in house.cables])
        y = np.array([cable.y for cable in house.cables])
        ax.plot(x, y, c='black', linewidth=0.5)

    # plot grid
    plt.xticks(np.arange(0, 51, step=1))
    plt.yticks(np.arange(0, 51, step=1))
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
    # mogelijk nog de totale kosten berekenen en ook in de legenda plaatsen

    # plot legend
    plt.legend(bbox_to_anchor=(0.75, 1.18), loc="upper left", handles=[cables, houses, batteries], framealpha=0.5)
