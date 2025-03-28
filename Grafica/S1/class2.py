import numpy as np
import cv2 as cv


def lin_inter(x1, y1, x2, y2, x):
    if x2 == x1:
        return y1
    return (x - x1) * (y2 - y1) / (x2 - x1) + y1

def bi_inter(x1, q11, x2, q21, y1, q12, y2, q22, x, y):
    r1 = lin_inter(x1, q11, x2, q21, x)
    r2 = lin_inter(x1, q12, x2, q22, x)
    return lin_inter(y1, r1, y2, r2, y)

def resize(image, new_width, new_height):
    height, width, dim = image.shape
    new_image = np.zeros((new_height, new_width, dim), dtype=np.uint8)

    for i in range(new_height):
        for j in range(new_width):
            x = j * (width - 1) / (new_width - 1) if new_width > 1 else 0
            y = i * (height - 1) / (new_height - 1) if new_height > 1 else 0

            x1 = int(np.floor(x))
            x2 = min(x1 + 1, width - 1)
            y1 = int(np.floor(y))
            y2 = min(y1 + 1, height - 1)

            # for c in range(dim):
            #     new_image[i, j, c] = bi_inter(
            #         x1, image[y1, x1, c],
            #         x2, image[y1, x2, c],
            #         y1, image[y2, x1, c],
            #         y2, image[y2, x2, c],
            #         x, y
            #     )

            new_image[i, j] = bi_inter(
                x1, image[y1, x1],
                x2, image[y1, x2],
                y1, image[y2, x1],
                y2, image[y2, x2],
                x, y
            )

    return new_image
# esconder un codigo en una image


img  = cv.imread('images.jpeg', -1) # 0 = gray, 1 = unchanged (with alpha), -1 = color (default, without alpha)
# img = cv.resize(img, (100, 100)) # resize to 100x100
# img = cv.resize(img, (0, 0), fx=0.5, fy=0.5) # resize by factor (half of the size)
# img = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE) # rotate 90 degrees clockwise
# img = np.array(
#     [[[255, 0, 0], [0, 255, 0]],
#      [[255, 255, 0], [255, 0, 255]]], dtype=np.uint8)

img_res = resize(img, 60, 60)
cv.imshow('image', img_res)
cv.waitKey(0)
cv.destroyAllWindows()
# cv.imwrite('cv_images.jpeg', img)
