import Variables as v

def drawBackground(screen, background):
    screen.fill(background)


warehouse_shelves_top = []
for i in range(v.SHELF_NUMBER):
    warehouse_shelves_top.append([(v.INITIAL_X - (i * v.INTER_SHELF_DISTANCE * v.PIXEL_SCALE),
                                   v.INITIAL_Y_TOP),
                                  (v.INITIAL_X - (i * v.INTER_SHELF_DISTANCE * v.PIXEL_SCALE),
                                   v.FINAL_Y_TOP)
                                  ])

warehouse_shelves_bottom = []
for i in range(v.SHELF_NUMBER):
    warehouse_shelves_bottom.append([(v.INITIAL_X - (i * v.INTER_SHELF_DISTANCE * v.PIXEL_SCALE),
                                      v.INITIAL_Y_BOTTOM),
                                     (v.INITIAL_X - (i * v.INTER_SHELF_DISTANCE * v.PIXEL_SCALE),
                                      v.FINAL_Y_BOTTOM)
                                     ])

warehouse_walls = [(v.INITIAL_X + 4 * v.PIXEL_SCALE, v.FINAL_Y_TOP + 1 * v.PIXEL_SCALE),
                   (v.INITIAL_X + 4 * v.PIXEL_SCALE, v.INITIAL_Y_TOP - 1 * v.PIXEL_SCALE),
                   (v.INITIAL_X - ((v.SHELF_NUMBER - 1) * v.INTER_SHELF_DISTANCE * v.PIXEL_SCALE) - 4 * v.PIXEL_SCALE,
                    v.INITIAL_Y_TOP - 1 * v.PIXEL_SCALE),
                   (v.INITIAL_X - ((v.SHELF_NUMBER - 1) * v.INTER_SHELF_DISTANCE * v.PIXEL_SCALE) - 4 * v.PIXEL_SCALE,
                    v.FINAL_Y_BOTTOM + 1 * v.PIXEL_SCALE),
                   (v.INITIAL_X + 4 * v.PIXEL_SCALE, v.FINAL_Y_BOTTOM + 1 * v.PIXEL_SCALE),
                   (v.INITIAL_X + 4 * v.PIXEL_SCALE, v.INITIAL_Y_BOTTOM - 1 * v.PIXEL_SCALE)
                   ]
