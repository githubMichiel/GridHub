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

def json_output():
    

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

    #print(district[0].houses)
    #print(district[0].batteries)
    #print(json_output())
    #parsed = json.loads(json_output())
    #print(json.dumps(parsed, indent=4))

    print(districts[0])
    print(districts[0].batteries[0])
    print(districts[0].houses[0])

    your_json = '["foo", {"bar": ["baz", null, 1.0, 2]}]'
    parsed = json.loads(your_json)
    print(json.dumps(parsed, indent=4))
