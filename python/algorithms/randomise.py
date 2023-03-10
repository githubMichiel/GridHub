import random

def random_algorithm(district, IS_UNIQUE_CABLES):
    """algorithm to randomly connect houses with batteries.
    runs until a valid solution is found.
    CAUTION: may run indefinitely."""

    # reset district before finding solutions
    district.clear_connections(cables_only=False)
    district.reset_costs()

    # run until a valid solution is found for a district
    while not district.all_houses_connected():
        # reset district if solution was not found
        district.clear_connections(cables_only=False)
        district.reset_costs()

        # loop over houses
        for house in district.houses:
            # choose a random battery
            random.shuffle(district.batteries)

            # create battery-house connection
            for battery in district.batteries:
                    if battery.check_capacity_limit(house.max_output):
                        house.set_battery(battery)
                        battery.add_usage(house.max_output)
                        break

    # when all houses are connected AND constraints are met, add cable connections
    for house in district.houses:
        house.add_cable_connection(house.battery)

    # make list of connected houses per battery
    district.list_houses_per_battery()

    # add all cables in a district to one list
    district.add_all_cables()

    # if cables are shared remove duplicates
    if IS_UNIQUE_CABLES == False:
        district.remove_duplicate_cables()

    # return cost per district
    return district.calculate_total_costs()
