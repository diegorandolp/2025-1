import numpy as np
import cv2 as cv
import os
def circle_blue():
    img = cv.imread('./lenna.png')
    height, width, dim = img.shape
    r = height // 2

    bg = np.full((height, width, dim), 255, np.uint8)
    h, w, d = bg.shape
    for i in range(h):
        for j in range(w):
            if (i - r) ** 2 + (j - r) ** 2 <= r**2:
                bg[i, j] = np.array([255, 0, 0])
    # scale color we want
    for i in range(height):
        for j in range(width):
                img[i, j] = bg[i, j] * (max(img[i][j])/max(bg[i, j]))

    route = './exercise04/output/lenna-colorscale.png'
    os.makedirs(os.path.dirname(route), exist_ok=True)
    cv.imwrite(route, img)
    return img
circle_blue()

