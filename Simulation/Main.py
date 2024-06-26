import os.path
import sys
import Facility
import utils
import Variables as v
import Visualization
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

##################################################################################################################

if __name__ == "__main__":

    data_dir = utils.getRelPath("data")
    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)

    try:
        Visualization.run(facility_1)
    except Exception as e:
        with open("log.txt", "w+") as log:
            log.write(repr(e))
            type, value, traceback = sys.exc_info()
            log.write('Error opening %s: %s' % (value.filename, value.strerror))
