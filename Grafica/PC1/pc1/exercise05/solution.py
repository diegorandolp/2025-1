import os
import numpy as np
import cv2 as cv

def box_filter(order):
    return np.array([[1/(order**2)]*order for i in range(order)])
def bartlett_filter(order):
    h1 = []
    for i in range(1, order//2 + 2):
        h1.append(i)
    for i in range(order//2, 0, -1):
        h1.append(i)
    factor = np.sum(h1) ** 2
    h2 = np.zeros((order, order))
    for i in range(order):
        for j in range(order):
            h2[i, j] = h1[i] * h1[j]
    h2 = h2 / factor
    return h2
def pascal(n):
    res = [[1]]
    for i in range(1, n):
        curr = [1] * (i + 1)
        res.append(curr)
        for j in range(1, i):
            res[i][j] = res[i - 1][j] + res[i - 1][j - 1]
    return res
def gaussian_filter(coef,order):
    h1 = coef[order - 1]
    h2 = np.zeros((order, order))
    factor = np.sum(h1) ** 2
    for i in range(order):
        for j in range(order):
            h2[i, j] = h1[i] * h1[j]

    h2 = h2 / factor
    return h2

def filter(kernel, img, path, isGray):
    img_ = img.copy()
    height, width, dim = img_.shape
    k_height, k_width = kernel.shape

    if isGray:
        k = [255, 255, 255]
        # grises
        k = np.array(k)
        for i in range(height):
            for j in range(width):
                img_[i][j] = k * (max(img_[i][j]) / max(k))
    n_pad_h = k_height //2
    n_pad_w = k_width //2

    img_mod = np.pad(img_, ((n_pad_h, n_pad_h), (n_pad_w, n_pad_w), (0, 0)), mode='symmetric')

    conv_x_lim = k_height // 2
    conv_y_lim = k_width // 2
    for i in range(height):
        for j in range(width):
            new_img = 0
            # img_area = img_mod[i-conv_y_lim:i+conv_y_lim+1,j-conv_x_lim:j+conv_x_lim+1]
            # img_area = img_area * kernel
            for m in range(-conv_y_lim, conv_y_lim + 1):
                for n in range(-conv_x_lim, conv_x_lim + 1):
                    img_nn_y = i + m
                    img_nn_x = j + n
                    new_img = new_img + kernel[m+conv_y_lim][n+conv_x_lim] * img_mod[img_nn_y][img_nn_x]
            # img_[i][j] = np.sum(img_area)
            img_[i, j] = new_img
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cv.imwrite(path, img_)

def solve(orders_):
    img = cv.imread('./lenna.png')
    coef_bin = pascal(25)
    name_filter = ['box', 'gaussian', 'bartlett']
    route = './exercise05/output/'
    for order in orders_:
        filters = [box_filter(order), gaussian_filter(coef_bin, order), bartlett_filter(order)]
        for i in range(3):
            path_ = route + name_filter[i] + '_' + str(order) + '.png'
            filter(filters[i], img, path_, False)
            path2_ = route + name_filter[i] + '_gray_' + str(order) + '.png'
            filter(filters[i], img, path2_, True)
def laplacian():
    kernels = [np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]]),
               np.array([[0,0,1,0,0],[0,1,2,1,0],[1,2,-17,2,1],[0,1,2,1,0],[0,0,1,0,0]])]
    orders = [3, 5]
    img = cv.imread('./lenna.png')
    for order in orders:
        for i in range(2):
            path_ = './exercise05/output/laplacian_' + str(order) + '.png'
            filter(kernels[i], img, path_, False)
            path2_ = './exercise05/output/laplacian_gray_' + str(order) + '.png'
            filter(kernels[i], img, path2_, True)
# print(box_filter(7))

# print(bartlett_filter(19))

# print(gaussian_filter(coef_bin, 5))

orders = [ 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25]

# orders = [ 3]
solve(orders)
laplacian()