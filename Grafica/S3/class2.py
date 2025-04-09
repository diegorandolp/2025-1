import numpy as np
import cv2 as cv
# mapeo de texturas - coordenadas baricentricas
def check_cell(cell):
    l = len(cell)
    for i in range(l):
        if cell[i] < 0:
            cell[i] = 0
        if cell[i] > 255:
            cell[i] = 255

def filter(kernel, img, mod):
    height, width, dim = img.shape
    k_height, k_width = kernel.shape
    k = [255, 255, 255]

    # grises
    k = np.array(k)
    for i in range(height):
        for j in range(width):
            img[i][j] = k * (max(img[i][j]) / max(k))


    cv.imshow('img_original', img)

    img_mod = np.pad(img, ((k_height-1, k_height-1), (k_width-1, k_width-1), (0, 0)), mode='symmetric')

    conv_x_lim = k_height // 2
    conv_y_lim = k_width // 2
    for i in range(height):
        for j in range(width):
            new_img = 0
            for m in range(-conv_y_lim, conv_y_lim + 1):
                for n in range(-conv_x_lim, conv_x_lim + 1):
                    img_nn_y = i + m
                    img_nn_x = j + n
                    new_img = new_img + kernel[m+conv_y_lim][n+conv_x_lim] * img_mod[img_nn_y][img_nn_x]
            if mod == "add":
                img[i][j] = img[i][j] + new_img
                check_cell(img[i][j])
            elif mod == "sub":
                img[i][j] = img[i][j] - new_img
                check_cell(img[i][j])
            else:
                img[i][j] = new_img

    cv.imshow('image_mod', img)
    cv.waitKey(0)
    cv.destroyAllWindows()


img = cv.imread('../S2/image2.jpg')
size_kernel = 5

# Box filter
# kernel = np.array([[1/(size_kernel**2)]*size_kernel for i in range(size_kernel)])

# Gaussian
# kernel = [[1, 2, 1], [2, 4, 2], [1, 2, 1]]
# for i in range(size_kernel):
#     for j in range(size_kernel):
#         kernel[i][j] = kernel[i][j] / 16
# kernel = np.array(kernel)

# Barlett
# kernel_1d = []
# lim_kernel_1d = size_kernel // 2
# for i in range(1, lim_kernel_1d + 2):
#     kernel_1d.append(i)
# for i in range(lim_kernel_1d, 0, -1):
#     kernel_1d.append(i)
# for el in kernel_1d:
#     for el2 in kernel_id:

# Laplacian
kernel = [[1, 1, 1], [1, -8, 1], [1, 1, 1]]

for i in range(size_kernel):
    for j in range(size_kernel):
        kernel[i][j] = kernel[i][j] / 25
kernel = np.array(kernel)

filter(kernel, img, mod="")