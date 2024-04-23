"""
Simulation variables

"""

NUM_WORKERS = 1  # Currently unable to visualize more than one worker

WORKER_SPEED_X = 1  # Don't set speeds below 0.5
WORKER_SPEED_Y = 1  # Don't set speeds below 0.5
WORKER_SPEED_Z = 0.5
WORKER_PICKING_TIME = 10

INTER_SHELF_DISTANCE = 4
INTER_COMPARTMENT_DISTANCE = 1
SHELF_NUMBER = 10
COMPARTMENT_NUMBER = 10

MTBO = 100.0  # Mean time between orders
SIM_TIME = 1000

# Visualization variables

FPS = 21.93  # Set to 21.93 for real time visualization
PIXEL_SCALE = 20

INITIAL_X = 1000
INITIAL_Y_TOP = 100
FINAL_Y_TOP = (INITIAL_Y_TOP +
               (INTER_COMPARTMENT_DISTANCE *
                COMPARTMENT_NUMBER *
                PIXEL_SCALE)
               )

INITIAL_Y_BOTTOM = (INITIAL_Y_TOP +
                    (INTER_COMPARTMENT_DISTANCE *
                     COMPARTMENT_NUMBER *
                     PIXEL_SCALE) +
                    (4 * PIXEL_SCALE)
                    )

FINAL_Y_BOTTOM = (INITIAL_Y_BOTTOM +
                  (INTER_COMPARTMENT_DISTANCE *
                   COMPARTMENT_NUMBER *
                   PIXEL_SCALE)
                  )
