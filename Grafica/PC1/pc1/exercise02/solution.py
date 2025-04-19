import numpy as np
import cv2 as cv

def chessboard_with_custom_colors(WIDTH_IN_PIXELS, HEIGHT_IN_PIXELS, NUM_OF_CELLS_HORIZONTAL, NUM_OF_CELLS_VERTICAL, COLORS):
    len_ = len(COLORS)
    img = np.zeros((HEIGHT_IN_PIXELS, WIDTH_IN_PIXELS, 3), np.uint8)
    step_h = WIDTH_IN_PIXELS // NUM_OF_CELLS_HORIZONTAL
    step_v = HEIGHT_IN_PIXELS // NUM_OF_CELLS_VERTICAL

    for i in range(NUM_OF_CELLS_VERTICAL):
        i1 = i * step_v
        i2 = (i + 1) * step_v - 1
        for j in range(NUM_OF_CELLS_HORIZONTAL):
            j1 = j * step_h
            j2 = (j + 1) * step_h - 1
            if step_h > 1 and step_v > 1: # if it is not 1x1px
                img[i1:i2, j1:j2] = np.full((step_v - 1, step_h - 1, 3), COLORS[(i+j) % len_])
            else:
                img[i, j] = COLORS[(i+j) % len_]
    return img.astype(np.uint8)
