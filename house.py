# create a class that describes a 'house' object

class House():

    def __init__(self, x, y, max_output):
        self.x = x
        self.y = y
        self.max_output = max_output
        self.battery = None


        # make list with corresponding cable location
        self.cables = []

    # set self.battery to a battery object
    def set_battery(self, battery):
        self.battery = battery

    # add cable connection between the house and a battery
    # picks a shortest route (this algorithm is for the unique cable case where it doesnt matter what shortest route we pick)
    def add_connection(self, battery):
        distance_x = self.x - battery.x
        distance_y = self.y - battery.y
        if distance_x >= 0:
            for i in range(abs(distance_x) + 1):
                self.cables.append((self.x - i, self.y))
        else:
            for i in range(abs(distance_x) + 1):
                self.cables.append((self.x + i, self.y))
        if distance_y >= 0:
            for i in range(abs(distance_y) + 1):
                self.cables.append((self.x - distance_x,self.y - i))
        else:
            for i in range(abs(distance_y) + 1):
                self.cables.append((self.x - distance_x,self.y + i))



#    def __repr__(self):
#        return f'{{"location": "{self.x},{self.y}","output": {self.max_output},"cables": []}}'
