import numpy as np
import cv2 as cv

def change_brightness(img, brightness):

    height, width, dim = img.shape

    for i in range(height):
        for j in range(width):
            img[i, j] = img[i, j] + brightness
            for k in range(dim):
                if img[i, j, k] > 255:
                    img[i, j, k] = 255

    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()
def get_m_M(img):

    m = [256] * 3
    M = [-1] * 3

    height, width, dim = img.shape
    if dim == 4:
        dim = dim - 1
    for i in range(height):
        for j in range(width):
            for k in range(dim):
                if img[i][j][k] < m[k]:
                    m[k] = img[i][j][k]
                if img[i][j][k] > M[k]:
                    M[k] = img[i][j][k]
    return m, M


def change_contrast(img, new_m, new_M):
    img = img.astype(np.float32)
    height, width, dim = img.shape

    m, M = get_m_M(img)

    if dim == 4:
        dim = dim - 1
    for i in range(height):
        for j in range(width):
            for k in range(dim):
                if M[k] != m[k]:
                    img[i][j][k] = new_m[k] + (new_M[k] - new_m[k])*(img[i][j][k]-m[k])/(M[k] - m[k])
    img = img.astype('uint8')
    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

img = cv.imread('lowcontrast.png', -1 )
# change_brightness(img, 20)
new_m = [0] * 3
new_M = [255] * 3
change_contrast(img, new_m, new_M)