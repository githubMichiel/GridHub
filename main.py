"""
smartgrid.py

-
"""

from battery import Battery
from house import House
from district import District

if __name__ == "__main__":

    # create districts
    districts = []
    for i in range(1,4):
        districts.append(District(i))
    districts[0].load_houses('district-1_houses.csv')
    districts[0].load_batteries('district-1_batteries.csv')
    districts[1].load_houses('district-2_houses.csv')
    districts[1].load_batteries('district-2_batteries.csv')
    districts[2].load_houses('district-3_houses.csv')
    districts[2].load_batteries('district-3_batteries.csv')

    
