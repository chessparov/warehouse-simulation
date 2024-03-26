import pygame
import Variables as v


class TWorker(pygame.sprite.Sprite):

    def __init__(self, screen, image, x: int, y: int, scale: float, x_speed: float, y_speed: float):
        super().__init__()
        self.x = x
        self.y = y
        self.x_travelled = round(float(0))
        self.y_travelled = round(float(0))
        self.scale = float(scale)
        self.x_speed = float(x_speed)
        self.y_speed = float(y_speed)

        self.screen = screen
        self.end = False
        self.reverse_end = False

        # Load worker image
        self.worker_image = pygame.transform.scale(image,
                                                   (int(image.get_width() * self.scale),
                                                    int(image.get_height() * self.scale))
                                                   )

        # Create an instance of the above image
        self.rect = self.worker_image.get_rect()
        self.rect.center = (self.x, self.y)

        # Flips image according to travelling direction
        self.direction = 1
        self.flip = False

    def point_move(self, coordinates):

        if self.end:
            return

        left = True
        right = False
        up = False
        down = False

        x_dist = coordinates[0][1] * v.PIXEL_SCALE * (v.INTER_SHELF_DISTANCE + 1)
        y_dist = coordinates[1][0] * v.PIXEL_SCALE * (v.INTER_COMPARTMENT_DISTANCE + 3)

        if round(self.x_travelled) == x_dist:
            left = False
            if coordinates[0][0]:
                up = True
            else:
                down = True

        if round(self.y_travelled) == y_dist:
            self.end = True
            up = False
            down = False
            self.x_travelled = 0.0
            self.y_travelled = 0.0

        dx = float(0)
        dy = float(0)

        if left:
            self.flip = False
            self.direction = 1
            if round(self.x_travelled) <= x_dist:
                dx = -self.x_speed
            else:
                pass

        if right:
            self.flip = True
            self.direction = -1
            if round(self.x_travelled) <= x_dist:
                dx = self.x_speed
            else:
                pass

        if up:
            if round(self.y_travelled) <= y_dist:
                dy = - self.y_speed
            else:
                pass
        if down:
            if round(self.y_travelled) <= y_dist:
                dy = self.y_speed
            else:
                pass

        # Updates the position of the rectangle
        self.rect.x += dx
        self.rect.y += dy

        self.x_travelled += round(abs(dx), 2)
        self.y_travelled += round(abs(dy), 2)

    def point_move_backwards(self, coordinates):

        if self.reverse_end:
            return

        left = False
        right = False
        up = False
        down = False

        if not coordinates[0][0]:
            up = True
        else:
            down = True

        x_dist = coordinates[0][1] * v.INTER_SHELF_DISTANCE * v.PIXEL_SCALE + 1 * v.PIXEL_SCALE
        y_dist = coordinates[1][0] * v.INTER_COMPARTMENT_DISTANCE * v.PIXEL_SCALE + 3 * v.PIXEL_SCALE

        if round(self.y_travelled) == y_dist:
            up = False
            down = False
            right = True

        if round(self.x_travelled) == x_dist:
            self.reverse_end = True
            self.x_travelled = 0.0
            self.y_travelled = 0.0
            left = False
            right = False
            up = False
            down = False

        dx = float(0)
        dy = float(0)

        if left:
            self.flip = False
            self.direction = 1
            if round(self.x_travelled) <= x_dist:
                dx = -self.x_speed
            else:
                pass

        if right:
            self.flip = True
            self.direction = -1
            if round(self.x_travelled) <= x_dist:
                dx = self.x_speed
            else:
                pass

        if up:
            if round(self.y_travelled) <= y_dist:
                dy = - self.y_speed
            else:
                pass
        if down:
            if round(self.y_travelled) <= y_dist:
                dy = self.y_speed
            else:
                pass

        # Updates the position of the rectangle
        self.rect.x += dx
        self.rect.y += dy

        self.x_travelled += round(abs(dx), 2)
        self.y_travelled += round(abs(dy), 2)

    def draw(self):

        self.screen.blit(pygame.transform.flip(self.worker_image, self.flip, False), self.rect)
