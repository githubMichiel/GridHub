import random

def greedy_algorithm(districts, IS_UNIQUE_CABLES):
    """algorithm to connect houses with batteries with greedy heuristic
    runs until a valid solution is found."""

    total_costs = []

    # loop over districts
    for district in districts:
        # reset district first
        district.reset_costs()
        district.clear_connections()

        # option 2: implement greedy cable connection (to closest battery)
        # sort houses based on output level
        district.houses.sort(key=lambda x: x.max_output, reverse=True)

        # loop over all (or x amount of) houses
        count_connected_houses = 0

        for house in district.houses:
            # determine closest battery and insert battery object
            closest_battery = None
            # maximum distance is 100
            shortest_distance = 101

            # loop over all batteries to search for shortest distance
            for battery in district.batteries:
                if battery.check_capacity_limit(house.max_output):
                    current_distance = district.calculate_distance(house, battery)

                    # if shorter distance and if adequate capacity set to current battery
                    if current_distance < shortest_distance:
                        shortest_distance = current_distance
                        closest_battery = battery

            # connect closest available battery to house
            if closest_battery != None:
                house.set_battery(closest_battery)
                closest_battery.add_usage(house.max_output)
                count_connected_houses += 1

        # print(f"Total connected houses step 1: {count_connected_houses}")

        # in case not all houses are connected swap battery connections
        if count_connected_houses != 150:
            # print("NOT 150 houses connected")

            # check battery input before swap
            # for battery in district.batteries:
            #     print(f"Battery {battery.id} input before swap: {battery.total_input}")

            # keep track of unconnected houses
            unconnected_houses = []
            for house in district.houses:
                if house.battery == None:
                    unconnected_houses.append(house)

            # print("list of unconnected houses: ", unconnected_houses)
            # for house in unconnected_houses:
            #     print("output of unconnected house: ", house.max_output)

            while count_connected_houses != 150:
                houses_index = range(100, 148)

                for x in houses_index:
                    swap_buddy = random.choice(houses_index)
                    while x == swap_buddy:
                        swap_buddy = random.choice(houses_index)

                    # swap battery of two houses
                    district.houses[x].swap_battery(district.houses[swap_buddy])

                    # if battery capacity is exceeded swap back
                    if district.houses[x].battery.total_input > district.houses[x].battery.capacity or district.houses[swap_buddy].battery.total_input > district.houses[swap_buddy].battery.capacity:
                        district.houses[x].swap_battery(district.houses[swap_buddy])

                    for battery in district.batteries:
                        free_space = battery.capacity - battery.total_input
                        for house in unconnected_houses:
                            if free_space >= house.max_output:
                                house.set_battery(battery)
                                battery.add_usage(house.max_output)
                                count_connected_houses += 1
                                unconnected_houses.remove(house)

        # if cables are shared remove duplicates
        if IS_UNIQUE_CABLES == False:
            district.remove_duplicate_cables()



            # this is a check to see if all houses are actually connected
            # unconnected_houses = []
            # for house in district.houses:
            #     if house.battery == None:
            #         unconnected_houses.append(house)
            # print("list of unconnected houses step 2: ", unconnected_houses)
            # print(f"Total connected houses step 2: {count_connected_houses}")
            #
            # for battery in district.batteries:
            #     print(f"Battery {battery.id} input after swap: {battery.total_input}")
            #
            # if district.check_capacity_constraint() is not True:
            #     print("Capacity constraint is NOT met")

# OPTION 4: greedy algorithm with connection to closest cable
            # print("OPTION 4: reconnect all houses to closest cables")
            # remove all cable connections but keep in memory which house is connected to which battery
            # district.remove_all_cables()
            for house in district.houses:
                house.cables = []

            # create list of all houses connected per battery
            district.list_houses_per_battery()

            # loop over all batteries to add cables BUT more efficient
            for battery in district.batteries:

                # calculate distances between house and batteries
                for house in battery.houses:
                    house.distance_to_batt = district.calculate_distance(house, battery)

                # sort houses based on distance to battery; closest house first
                battery.houses.sort(key=lambda x: x.distance_to_batt)

                # -- check to see if houses are sorted right --
                # print("print distance of house to battery: ", [house.distance_to_batt for house in battery.houses])

                # make list to keep track which houses are cable connected to a battery
                cable_connected_houses = []

                # loop over houses connected to that battery; start at nearest house
                for house in battery.houses:
                    # connect closest house directly to battery
                    if len(cable_connected_houses) == 0:
                        house.add_cable_connection(battery)
                        cable_connected_houses.append(house)

                    # connect the other houses to the closest cable connection
                    else:
                        closest_cable = None # cable object
                        closest_distance = 101
                        # loop over all cable connected houses to find the nearest cable
                        for cable_connected_house in cable_connected_houses:
                            for existing_cable in cable_connected_house.cables:
                                distance_house_cable = district.calculate_distance(house, existing_cable)
                                if distance_house_cable < closest_distance:
                                    closest_distance = distance_house_cable
                                    closest_cable = existing_cable

                        # add house to closest cable
                        house.add_cable_connection(closest_cable)
                        cable_connected_houses.append(house)
                        # print("Look for closest connection of house: ", house)
                        # print("Closest cable: ", closest_cable)
                        # print("Distance house to closest cable: ", closest_distance)

            # add all cables into the district
            district.add_all_cables()

        else:
            # when all houses are connected AND constraints are met, add cable connections
            for house in district.houses:
                house.add_cable_connection(house.battery)

            # make list of connected houses per battery
            district.list_houses_per_battery()

            # add all cables in a district to one list
            district.add_all_cables()
        # calculate cost per district
        total_costs.append(district.calculate_total_costs())

    # return cost per district
    return total_costs
