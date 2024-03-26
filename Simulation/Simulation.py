import os
import sys
import random
import simpy
import pandas as pd
import Facility
import Orders
import Variables as v

intOrders = int(0)
intPendingItems = int(0)
intTotalItems = int(0)
lstOrders = []
lstOrdersItems = []
order_data = []
items_data = []

dtfFinalAnalysis = pd.DataFrame([],
                                columns=["Number of orders",
                                         "Number of items",
                                         "Pending items"
                                         ])


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
        if not os.path.exists(os.path.join(base_path, "data")):
            os.mkdir(os.path.join(base_path, "data"))
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Wait for the time to pick the necessary object
def pickItem(env, facility, art: str, resource):
    global intPendingItems
    global items_data

    item_coordinates = facility.getPosition(art)

    x_dist = item_coordinates[0][1] * v.INTER_SHELF_DISTANCE * 2 + 1
    y_dist = item_coordinates[1][0] * v.INTER_COMPARTMENT_DISTANCE * 2 + 3
    z_dist = item_coordinates[1][1] * v.INTER_COMPARTMENT_DISTANCE * 2

    pick_time = (x_dist / v.WORKER_SPEED_X + y_dist / v.WORKER_SPEED_Y
                 + z_dist / v.WORKER_SPEED_Z + v.WORKER_PICKING_TIME)

    with resource.request() as req:
        yield req
        start_time = round(env.now, 1)
        print(f'{env.now:8.1f} s: Picking item {art}')

        yield env.timeout(pick_time)
        end_time = round(env.now, 1)
        print(f'{env.now:8.1f} s: Item {art} Delivered')
        # Refresh the pending items queue
        intPendingItems -= 1

    data = [art, item_coordinates[0][0],
            item_coordinates[0][1],
            item_coordinates[1][0],
            item_coordinates[1][1],
            start_time, end_time
            ]
    items_data.append(data)


def processOrder_by_item(env, items, facility):
    workers = simpy.Resource(env, v.NUM_WORKERS)

    while True:
        if items:
            for art in items:
                if facility.checkItem(art):
                    env.process(pickItem(env, facility, art, workers))
                    items.remove(art)
                else:
                    print(f'Item {art} not in inventory!')
        else:
            yield env.timeout(1)


# Periodically generates new orders
def generateOrder(env, facility):
    global lstOrders
    global lstOrdersItems
    global order_data
    global intOrders
    global intTotalItems
    global intPendingItems

    lstOrdersItems = []

    def orderGenerator(facility):

        lstItems = []
        item_count = random.randint(1, 5)

        if isinstance(facility, Facility.TFacility):
            while item_count > 0:
                art_number = random.randint(1, 1999)
                item_name = 'art' + str(art_number)
                lstItems.append(item_name)
                item_count -= 1
            return Orders.TOrder(lstItems)
        else:
            return 'Invalid facility! '

    while True:

        time = max(20.0, random.normalvariate(v.MTBO, 40.0))

        order = orderGenerator(facility)
        lstOrders.append(order)

        # Adding single items to another list
        for item in order.getArtlist():
            lstOrdersItems.append(item)

        print(f'{env.now:8.1f} s: Order {order.getUuid()} received')
        print(f"{'':12}Items requested: ")
        print(f"{'':12}" + ' '.join(str(x) for x in order.getArtlist()))

        data = [order.getUuid(), round(env.now, 1), len(order.getArtlist()), order.getArtlist()]
        order_data.append(data)

        intOrders += 1
        intTotalItems += len(order.getArtlist())
        intPendingItems += len(order.getArtlist())
        yield env.timeout(time)


def runSimulation(facility):
    global lstOrders
    global dtfFinalAnalysis
    global items_data
    global order_data
    global intOrders
    global intPendingItems
    global intTotalItems

    intOrders = int(0)
    intPendingItems = int(0)
    intTotalItems = int(0)
    order_data = []
    items_data = []

    if not isinstance(facility, Facility.TFacility):
        return 'Invalid facility! '

    env = simpy.Environment()
    print(f'Starting simulation at {env.now:.2f}')

    env.process(generateOrder(env, facility))
    env.process(processOrder_by_item(env, lstOrdersItems, facility))

    env.run(until=v.SIM_TIME)

    facility.setLoglist(order_data)
    facility.saveLog()

    dtfItems = pd.DataFrame(items_data, columns=['Item',
                                                 'Position',
                                                 'Shelf',
                                                 'Row',
                                                 'Column',
                                                 'Pick Time',
                                                 'Deliver Time'])

    path = resource_path(''.join([facility.getPath(), 'items_log.csv']))
    dtfItems.to_csv(path_or_buf=path,
                    index=False)

    # Analyze data
    print(f'\n{"-" * 40}\n'
          f'Total orders received: {intOrders}\n'
          f'Total items requested: {intTotalItems}\n'
          f'Pending Items: {intPendingItems}\n'
          f'{"-" * 40}')

    # Save analyzed data
    dtfAnalysis = pd.DataFrame({"Number of orders": [intOrders],
                                "Number of items": [intTotalItems],
                                "Pending items": [intPendingItems],
                                })

    dtfFinalAnalysis = pd.concat([dtfFinalAnalysis, dtfAnalysis], ignore_index=True)
