import numpy as np
import cv2 as cv


def change_contrast(img, percent):
    percent = percent - 100
    img_ = img.copy()
    if percent == 0:
        return img_

    m = img_.min(axis=(0, 1))
    M = img_.max(axis=(0, 1))

    if percent < 0:
        percent = -percent
        step = ((M-m)*0.5) * (percent / 100)
        new_m = m + step
        new_M = M + 1 - step
    else:
        step_left = m * (percent / 100)
        new_m =  m - step_left

        step_right = (255 - M) * (percent / 100)
        new_M = M + step_right

    m = np.full(3, m)
    M = np.full(3, M)

    r2 = (new_M - new_m) / (M - m)
    img_ = new_m + (img_ - m) * r2
    return img_.astype(np.uint8)
def on_trackbar(val):
    img_ = change_contrast(img, val)
    cv.imshow(title_window, img_)


# percent goes from -100 to 100


img = cv.imread('lowcontrast.png')
alpha_slider_max = 200
title_window = 'Contraste'
cv.namedWindow(title_window)
trackbar_name = 'Contrast %d' % alpha_slider_max
cv.createTrackbar(trackbar_name, title_window , 100, alpha_slider_max, on_trackbar)
cv.waitKey()
cv.destroyAllWindows()
