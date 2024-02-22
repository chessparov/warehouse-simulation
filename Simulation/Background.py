import Variables as v


def drawBackground(screen, background):
    screen.fill(background)


# Constants
UNIT = 1 * v.PIXEL_SCALE
INTER_SHELF = v.INTER_SHELF_DISTANCE * UNIT
RIGHT_X = v.INITIAL_X + 4 * UNIT
LEFT_X = v.INITIAL_X - ((v.SHELF_NUMBER - 1) * INTER_SHELF) - 4 * UNIT

warehouse_shelves_top = []

for i in range(v.SHELF_NUMBER):
    warehouse_shelves_top.append([(v.INITIAL_X - (i * INTER_SHELF),
                                   v.INITIAL_Y_TOP),
                                  (v.INITIAL_X - (i * INTER_SHELF),
                                   v.FINAL_Y_TOP)
                                  ])

warehouse_shelves_bottom = []
for i in range(v.SHELF_NUMBER):
    warehouse_shelves_bottom.append([(v.INITIAL_X - (i * INTER_SHELF),
                                      v.INITIAL_Y_BOTTOM),
                                     (v.INITIAL_X - (i * INTER_SHELF),
                                      v.FINAL_Y_BOTTOM)
                                     ])

# Warehouse external coordinates
top_door_wall = (RIGHT_X, v.FINAL_Y_TOP + UNIT)
top_right_wall = (RIGHT_X, v.INITIAL_Y_TOP - UNIT)
top_left_wall = (LEFT_X, v.INITIAL_Y_TOP - UNIT)
bottom_left_wall = (LEFT_X, v.FINAL_Y_BOTTOM + UNIT)
bottom_right_wall = (RIGHT_X, v.FINAL_Y_BOTTOM + UNIT)
bottom_door_wall = (RIGHT_X, v.INITIAL_Y_BOTTOM - UNIT)

warehouse_walls = [top_door_wall,
                   top_right_wall,
                   top_left_wall,
                   bottom_left_wall,
                   bottom_right_wall,
                   bottom_door_wall
                   ]
