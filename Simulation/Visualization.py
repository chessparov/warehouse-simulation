import pygame
import ctypes
import sys
import pandas as pd
from pathlib import Path
import Worker
import Background
import Variables as v
import GUI

# Checks whether if the OS is windows in order to apply
# the taskbar icon correctly
if 'win' in sys.platform:
    win_id = u'DES.1.0'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(win_id)

running = True
elapsed_time = 0


def run():

    global running
    global elapsed_time

    pygame.init()

    # Set window title
    pygame.display.set_caption('Warehouse DES')

    # Create an icon
    icon = pygame.image.load(r'Images/Icon.jpg')
    pygame.display.set_icon(icon)

    # Set screen size
    screen = pygame.display.set_mode((1280, 720))

    # Limit framerate
    clock = pygame.time.Clock()
    end_time = 0

    # Import items to pick
    path_name = Path(r'.\Test\items_log.csv')
    dtfData = pd.read_csv(path_name)
    coordinates = []
    for i in dtfData.index:
        tpl1 = (dtfData['Position'][i], dtfData['Shelf'][i])
        tpl2 = (dtfData['Row'][i], dtfData['Column'][i])
        coordinates.append([tpl1, tpl2])

    i = 0

    # Create objects
    worker_image = pygame.image.load(r'Images/MFN_worker2.gif')
    box_image = pygame.image.load(r'Images/Box.png')
    worker = Worker.TWorker(screen, worker_image, 'worker', (v.INITIAL_X + 3 * v.PIXEL_SCALE),
                            340, 0.1, v.WORKER_SPEED_X, v.WORKER_SPEED_Y)

    # Start GUI info
    app = GUI.QApplication(sys.argv)

    # Info window
    win = GUI.TMainWindow()
    win.show()

    # Handles the exit procedure
    def myExitHandler():

        pygame.quit()
        sys.exit(app.exec_())

    while running:

        # Set FPS
        clock.tick(v.FPS)

        # Graphics
        Background.drawBackground(screen, 'White')
        for top_shelf in Background.warehouse_shelves_top:
            pygame.draw.lines(screen, 'black', False, top_shelf)
        for bot_shelf in Background.warehouse_shelves_bottom:
            pygame.draw.lines(screen, 'black', False, bot_shelf)
        pygame.draw.lines(screen, 'black', False, Background.warehouse_walls, width=5)

        # Worker animation
        worker.draw()

        # Start timer for timeouts
        current_time = pygame.time.get_ticks() * (v.FPS / 21.93)
        elapsed_time = current_time
        win.beginTimer()

        # Variable used to check if i has changed
        j = i

        # Make the worker move and pick the box
        if i < len(coordinates):

            # Iterative coordinates
            coordinate = coordinates[i]
            z_dist = coordinate[1][1] * v.INTER_COMPARTMENT_DISTANCE * 2
            x_dist = coordinate[0][1] * v.INTER_SHELF_DISTANCE + 1
            y_dist = coordinate[1][0] * v.INTER_COMPARTMENT_DISTANCE + 3

            worker.point_move(coordinate)
            # When the first leg of the path has been walked
            if worker.end:
                # Wait for the z axis climb
                if (current_time - end_time) < (int(z_dist / v.WORKER_SPEED_Z +
                                                    x_dist / v.WORKER_SPEED_X +
                                                    y_dist / v.WORKER_SPEED_Y +
                                                    v.WORKER_PICKING_TIME) * 1000):
                    pass

                else:
                    # Draw the box
                    box = Worker.TWorker(screen, box_image,
                                         'box',
                                         worker.rect.x + 3,
                                         worker.rect.y + 20,
                                         0.03,
                                         v.WORKER_SPEED_X,
                                         v.WORKER_SPEED_Y)
                    box.draw()

                    # Begin moving backwards
                    worker.point_move_backwards(coordinate)
                    box.point_move_backwards(coordinate)

                    # When the end is reached
                    if worker.reverse_end:
                        i += 1
                        end_time = current_time

        # End reached, re-initialize worker
        if j != i:
            worker = Worker.TWorker(screen, worker_image,
                                    'worker',
                                    (v.INITIAL_X + 3 * v.PIXEL_SCALE),
                                    340, 0.1,
                                    v.WORKER_SPEED_X,
                                    v.WORKER_SPEED_Y)

        # Quit the simulation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()

    pygame.quit()
    app.aboutToQuit.connect(myExitHandler)




