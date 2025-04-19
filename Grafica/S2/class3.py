import numpy as np
import cv2 as cv

def grises(img, k):
    height, width, dim = img.shape
    # scale color we want
    k = np.array(k)
    for i in range(height):
        for j in range(width):
            img[i][j] = k * (max(img[i][j])/max(k))


    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()
def random_sections(img, k):



    height, width, dim = img.shape

    step_x = int(width/2)
    step_y = int(height/2)

    k = np.array(k)
    for m in range(2):
        for n in range(2):
            for i in range(m*step_y, (m+1)*step_y):
                for j in range(n*step_x, (n+1)*step_x):
                    img[i][j] = k[m][n] * (max(img[i][j])/max(k[m][n]))


    cv.imshow('image', img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def scale_img(to_image, from_image, flag):
    to_dims = to_image.shape
    from_dims = from_image.shape

    for i in range(to_dims[0]):
        for j in range(from_dims[1]):
            if flag :
                if np.argmax(to_image[i][j])==1:
                    to_image[i][j] = from_image[i][j]
                else:
                    continue
            to_image[i][j] = from_image[i][j] * (max(to_image[i][j]) / max(from_image[i][j]))
    cv.imshow('to_image', to_image)
    cv.imshow('from_image', from_image)
    cv.waitKey(0)
    cv.destroyAllWindows()




new_scale = [255, 255, 255]
img = cv.imread('green.jpg')
height, width, dim = img.shape
cv.imshow('image0', img)

grises(img, new_scale)

# new_scale_section= [ [[255, 53, 32], [0, 255, 0]], [[0, 255, 0], [0, 0, 255]] ]
#
# random_sections(img, new_scale_section)

# src_image = cv.imread('image2.jpg')
# src_image = cv.resize(src_image, (width, height))
#
# scale_img(img, src_image, 1)