import numpy as np
import pygame as pg
import random

class Pixel:
    def __init__(self, pos, color):
        self.pos = pos
        self.color = color
        self.direction = DIRECTIONS[random.choice([0, 1, 2, 3])]

    def move(self):
        if 0 <= (self.pos + 5 * self.direction)[0] <= WIDTH and 0 <= (self.pos + 5 * self.direction)[1] <= LENGTH:
            self.pos += 5 * self.direction
        self.direction = DIRECTIONS[np.random.choice([0, 1, 2, 3])]

    def paint(self, surf):
        x1, y1 = self.pos + 5*self.direction
        pg.draw.line(surf, self.color, self.pos, (x1, y1))


if __name__ == "__main__":
    N_PIXELS = 50
    WIDTH = 500
    LENGTH = 500
    DIRECTIONS = np.array([[0, 1], [-1, 0], [1, 0], [0, -1]])
    POS0 = np.array([WIDTH // 2, LENGTH // 2])

    pg.init()
    screen = pg.display.set_mode((WIDTH, LENGTH))
    clock = pg.time.Clock()
    running = True
    screen.fill("black")

    pixels = np.empty(N_PIXELS, dtype=Pixel)

    for i in range(N_PIXELS):
        pixels[i] = Pixel(POS0 + (i*2), (255, int(255*i/N_PIXELS), 0))

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # screen.fill("purple")
        for i in range(N_PIXELS):
            pixels[i].paint(screen)
            pixels[i].move()

        pg.display.flip()
        clock.tick(30)

    pg.quit()
