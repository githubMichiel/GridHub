# create a class that describes a 'house' object

class House():

    def __init__(self, x, y, maxoutput):
        self.x = x
        self.y = y
        self.maxoutput = maxoutput
        self.battery = None

        # location of the house
        self.location = f"{self.x}, {self.y}"

        # make list with corresponding cable location
        self.cables = []

    # set self.battery to a battery object
    def set_battery(self, battery):
        self.battery = battery

    def __str__(self):
        return f'["location": "{self.x},{self.y}","output": {self.maxoutput},"cables": {self.cables}]'
