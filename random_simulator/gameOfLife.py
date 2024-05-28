import numpy as np
import random
import pygame as pg
from PIL import Image


def rule(sub_mat):
    result = False
    # if sum(sub_mat[0:3:1, 0:3:1]) == 3 or sum(sub_mat[3:0:-1, 3:0:-1]) == 3:
    #     result = False
    neighbour_sum = sum(sub_mat[0, :]) + sum(sub_mat[2, :]) + sum(sub_mat[1, ::2])
    return ((sub_mat[1, 1] and neighbour_sum == 2) or (sub_mat[1, 1] and neighbour_sum == 3) or
            (not sub_mat[1, 1] and neighbour_sum == 3))


def update_matrix(full_mat):
    temp_mat = full_mat.copy()
    for i in range(1, full_mat.shape[0] - 1):
        for j in range(1, full_mat.shape[1] - 1):
            temp_mat[i, j] = rule(full_mat[i - 1:i + 2, j - 1:j + 2])
    return temp_mat


def display(mat, surf):
    for i in range(mat.shape[0]):
        x = i * 5
        for j in range(mat.shape[1]):
            y = j * 5
            c = mat[i, j] * np.array([255, 255, 255])
            pg.draw.rect(surf, c, pg.Rect(x, y, 5, 5))


if __name__ == "__main__":

    img = Image.open("initial_matrix.png")
    pix = img.load()
    WIDTH, LENGTH = img.size
    print(pix[0, 0])
    MATRIX = np.full((100, 100), False, dtype=bool)
    for i in range(WIDTH):
        for j in range(LENGTH):
            MATRIX[i, j] = not pix[i, j] == (255, 255, 255, 255)

    pg.init()
    screen = pg.display.set_mode((WIDTH * 5, LENGTH * 5))
    clock = pg.time.Clock()
    running = True
    screen.fill("purple")

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        display(MATRIX, screen)
        pg.display.flip()
        MATRIX = update_matrix(MATRIX)
        clock.tick(5)

    pg.quit()
