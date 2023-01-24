def connect_house_battery(self, IS_RANDOM_ALGORITHM, IS_UNIQUE_CABLES):
        """ connect each house to a battery depending on the chosen algorithm"""
        print(IS_RANDOM_ALGORITHM)
        i = 0
        # option 1: implement random cable connection
        if IS_RANDOM_ALGORITHM == True:
            is_all_connected = self.random_connect()

            # continue until all houses are connected
            while is_all_connected == False:
                i += 1
                print("i is", i)
                self.clear_connections()
                is_all_connected = self.random_connect()

        # option 2: implement greedy cable connection (to closest battery)
        else:
            # sort houses based on output level
            self.houses.sort(key=lambda x: x.max_output, reverse=True)

            # loop over all (or x amount of) houses
            count_connected_houses = 0

            for house in self.houses:
                # determine closest battery and insert battery object
                closest_battery = None
                # maximum distance is 100
                shortest_distance = 101

                # loop over all batteries to search for shortest distance
                for battery in self.batteries:
                    if battery.check_capacity_limit(house.max_output):
                        current_distance = self.calculate_distance(house, battery)

                        # if shorter distance and if adequate capacity set to current battery
                        if current_distance < shortest_distance:
                            shortest_distance = current_distance
                            closest_battery = battery

                # connect closest available battery to house
                if closest_battery != None:
                    house.set_battery(closest_battery)
                    closest_battery.add_input(house.max_output)
                    count_connected_houses += 1

            print(f"Total connected houses step 1: {count_connected_houses}")

            # in case not all houses are connected swap battery connections
            if count_connected_houses != 150:
                print("NOT 150 houses connected")

                # -- this is a check --
                # for battery in self.batteries:
                    # print(f"Battery {battery.id} input before swap: {battery.total_input}")

                # keep track of unconnected houses
                unconnected_houses = []
                for house in self.houses:
                    if house.battery == None:
                        unconnected_houses.append(house)

                print("list of unconnected houses: ", unconnected_houses)
                for house in unconnected_houses:
                    print("output of unconnected house: ", house.max_output)

                while count_connected_houses != 150:
                    houses_index = range(100, 148)

                    for x in houses_index:
                        swap_buddy = random.choice(houses_index)
                        while x == swap_buddy:
                            swap_buddy = random.choice(houses_index)

                        # swap battery of two houses
                        self.houses[x].swap_battery(self.houses[swap_buddy])

                        # if battery capacity is exceeded swap back
                        if self.houses[x].battery.total_input > self.houses[x].battery.capacity or self.houses[swap_buddy].battery.total_input > self.houses[swap_buddy].battery.capacity:
                            self.houses[x].swap_battery(self.houses[swap_buddy])

                        for battery in self.batteries:
                            free_space = battery.capacity - battery.total_input
                            for house in unconnected_houses:
                                if free_space >= house.max_output:
                                    house.set_battery(battery)
                                    battery.add_input(house.max_output)
                                    count_connected_houses += 1
                                    unconnected_houses.remove(house)

            # this is a check to see if all houses are actually connected
            unconnected_houses = []
            for house in self.houses:
                if house.battery == None:
                    unconnected_houses.append(house)
            print("list of unconnected houses AFTER swap: ", unconnected_houses)
            print(f"Total connected houses AFTER swap: {count_connected_houses}")

            # -- this is a check --
            for battery in self.batteries:
                print(f"Battery {battery.id} input after swap: {battery.total_input}")

            if self.check_capacity_constraint() is not True:
                print("Capacity constraint is NOT met")

            # OPTION 4: greedy algorithm with connection to closest cable
            if not IS_UNIQUE_CABLES:
                print("OPTION 4: reconnect all houses to closest cables")
                # remove all cable connections but keep in memory which house is connected to which battery
                for house in self.houses:
                    house.cables = []

                # create list of all houses connected per battery
                self.list_houses_per_battery()

                # loop over all batteries to add cables BUT more efficient
                for battery in self.batteries:

                    # calculate distances between house and batteries
                    for house in battery.houses:
                        house.distance_to_batt = self.calculate_distance(house, battery)

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
                            house.add_connection(battery)
                            cable_connected_houses.append(house)

                        # connect the other houses to the closest cable connection
                        else:
                            closest_cable = None # cable object
                            closest_distance = 101
                            # loop over all cable connected houses to find the nearest cable
                            for cable_connected_house in cable_connected_houses:
                                for existing_cable in cable_connected_house.cables:
                                    distance_house_cable = self.calculate_distance(house, existing_cable)
                                    if distance_house_cable < closest_distance:
                                        closest_distance = distance_house_cable
                                        closest_cable = existing_cable

                            # add house to closest cable
                            house.add_connection(closest_cable)
                            cable_connected_houses.append(house)
                            # print("Look for closest connection of house: ", house)
                            # print("Closest cable: ", closest_cable)
                            # print("Distance house to closest cable: ", closest_distance)

                for battery in self.batteries:
                    print("total amount of houses per battery: ", len(battery.houses))
