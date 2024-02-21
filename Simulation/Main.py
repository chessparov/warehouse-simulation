import Facility
import Variables as v
import Visualization
import Simulation
import numpy as np

# Creating a test facility
facility_1 = Facility.TFacility('facility_1', v.SHELF_NUMBER)

# Let's create an inventory
art_list = list()
for i in range(2000):
    art = Facility.TItem('art' + str(i + 1), np.random.uniform(0.10, 10),
                         np.random.uniform(0.01, 1))
    art_list.append(art)

# Add the items to the facility
facility_1.setItems(art_list)

#######################################################################################################

if __name__ == "__main__":

    Simulation.runSimulation(facility_1)
    Visualization.run()
