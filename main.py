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

def json_format(district):
    district_info = repr(district)
    #TODO: find a way to do this for all batteries without hard coding it
    batteries = [repr(district.batteries[0]),repr(district.batteries[1]),repr(district.batteries[2]),repr(district.batteries[3]),repr(district.batteries[4])]
    return f'[{{{district_info}}}, {{{batteries[0]}}}, {{{batteries[1]}}}, {{{batteries[2]}}}, {{{batteries[3]}}}, {{{batteries[4]}}}]'

def json_output(string):
    parsed = json.loads(string)
    print(json.dumps(parsed,indent=2))


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

    test = json_format(districts[0])
    json_output(test)
