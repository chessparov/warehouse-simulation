import simpy

import Facility
import Orders
import Picker
import numpy as np

# Let's create an inventory in a test Facility
facility_1 = Facility.TFacility('facility_1', 10)

art_list = list()
for i in range(2000):
    art = Facility.TItem('art' + str(i + 1), np.random.uniform(0.10, 10), np.random.uniform(0.01, 1))
    art_list.append(art)

# Add the items in storage
facility_1.setItems(art_list)

order1 = Orders.TOrder(art_list[46], art_list[83], art_list[998])

print(f'Starting simulation')

env = simpy.Environment()

for item in order1.getArtlist():
    env.process(Picker.setup(env, Picker.NUM_WORKERS, facility_1, item))

env.run()
