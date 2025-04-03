from pickletools import uint8
from time import sleep

import numpy as np
import cv2 as cv

def chess():
    cell = 10
    width = 500
    height = 500

    img = np.zeros((height, width, 3), np.uint8)
    step = width // cell

    curr_color = 0
    colors = {
        0: [255, 255, 255],
        1: [0, 0, 0],
    }
    for i in range(cell):
        i1 = i * step
        i2 = (i + 1) * step - 1
        for j in range(cell):
            j1 = j * step
            j2 = (j + 1) * step - 1
            if step != 1:
                # img[i1:i2, j1:j2] = np.full((step - 1, step - 1, 3), colors[curr_color])
                img[i1:i2, j1:j2] = np.full((step - 1, step - 1, 3), np.random.randint(256, size=3))
            else:
                img[i, j] = colors[curr_color]
            if j != cell - 1:
                curr_color = 1 if (curr_color == 0) else 0

    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()
# pending
def circle(n, radius):
    img = np.zeros((n, n, 3))

    center_x = n//2
    center_y = n//2

    for i in range(n):
        for j in range(n):
           if (i - center_x) ** 2 + (j - center_y) ** 2 <= radius ** 2:
               img[i, j] = [32,32,32]
    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def ev(real, im):
    c = complex(real, im)
    z = complex(0, 0)
    MAX_VALUE = 2
    for step in range(10**3):
        if abs(z) > MAX_VALUE:
            return [step] * 3
        try:
            z= z*z + c
        except:
            z = c

    return [255, 255, 255]


def fractal(n):
    x_dom = np.linspace(-2, 2, n)
    y_dom = np.linspace(-2, 2, n)
    img = []

    for i in y_dom:
        row = []
        for j in x_dom:
                row.append(ev(i, j))
        img.append(row)


    img = np.array(img)
    cv.imshow('image', img.astype(np.uint8))
    cv.waitKey(0)
    cv.destroyAllWindows()

def animation1():
    m = 500
    img = np.zeros((m, m, 3))
    n = 60
    radius = 30

    ball = np.zeros((n, n, 3))

    center_x = n // 2
    center_y = n // 2

    for i in range(n):
        for j in range(n):
            if (i - center_x) ** 2 + (j - center_y) ** 2 <= radius ** 2:
                ball[i, j] = [32, 32, 32]
    for i in range(20):
        img[i:n + i, 0:n, :] = ball
        cv.imshow('image', img)
        cv.destroyAllWindows()
        sleep(1)

    cv.waitKey(0)
# chess()
# circle(100, 30)
fractal(300)
# animation1()
