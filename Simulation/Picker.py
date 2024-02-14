import Facility
import Orders
import simpy

NUM_WORKERS = 1
WORKER_SPEED_X = 1
WORKER_SPEED_Y = 1
WORKER_SPEED_Z = 0.5
INTER_SHELF_DISTANCE = 4
INTER_COMPARTMENT_DISTANCE = 1

intPendingOrders = int(0)
intTotalOrders = int(0)

class Picker:

    def __init__(self, env, workers, facility):
        self.env = env
        self.workers = simpy.Resource(env, workers)
        if isinstance(facility, Facility.TFacility):
            self.facility = facility
        else:
            print('Please insert a valid Facility! ')

    def pickItem(self, art: str):

        global INTER_SHELF_DISTANCE
        global INTER_COMPARTMENT_DISTANCE
        global WORKER_SPEED_X
        global WORKER_SPEED_Y
        global WORKER_SPEED_Z

        item_coordinates = self.facility.getPosition(art)

        x_dist = item_coordinates[0][1]*INTER_SHELF_DISTANCE*2
        y_dist = item_coordinates[1][0]*INTER_COMPARTMENT_DISTANCE*2
        z_dist = item_coordinates[1][1]*INTER_COMPARTMENT_DISTANCE*2

        pick_time = (x_dist/WORKER_SPEED_X + y_dist/WORKER_SPEED_Y + z_dist/WORKER_SPEED_Z)
        print(f'Picking item at {self.env.now:.2f}')
        yield self.env.timeout(pick_time)
        print(f'Item Delivered at {self.env.now:.2f}')

def orderItem(env, art: str, picker):

    global intTotalOrders

    with picker.workers.request as request:
        yield request
        print(f'Item requested at {env.now:.2f}')
        yield env.process(picker.pickItem(art))
        print(f'Order satisfied at {env.now:.2f}')
        intTotalOrders += 1

def setup(env, workers: int, facility, art: str):

    if isinstance(facility, Facility.TFacility):
        picker = Picker(env, workers, facility)
    else:
        print('Insert a valid facility! ')

    while True:
        env.process(orderItem(env, art, picker))