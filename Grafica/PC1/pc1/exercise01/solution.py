import numpy as np

def lin_inter(x1, y1, x2, y2, x):
    if x2 == x1:
        return y1
    m = (y2 - y1) / (x2 - x1)
    res = m * (x - x1) + y1
    return np.clip(res, 0, 255)

def bi_inter(x1, x2, y1, y2, c11, c12, c21, c22, x, y):
    r1 = lin_inter(x1, c11, x2, c12, x) # horizontal
    r2 = lin_inter(x1, c21, x2, c22, x) # horizontal
    return lin_inter(y1, r1, y2, r2, y) # vertical

def resize(InputImage, NEW_WIDTH, NEW_HEIGHT, PADDING_STRATEGY):
    padding_pixels = 1
    shape = InputImage.shape
    image_ = InputImage
    reduce_dim = False
    if len(shape) == 2:
        image_ = np.expand_dims(image_, axis=-1)
        reduce_dim = True
    height, width, dim = image_.shape
    new_image = np.zeros((NEW_HEIGHT, NEW_WIDTH, dim), dtype=np.uint8)
    # PADDING
    pad_image = image_
    if PADDING_STRATEGY == 'ZEROS':
        pad_image = np.pad(image_, ((padding_pixels, padding_pixels), (padding_pixels, padding_pixels), (0, 0)), 'constant', constant_values=0)
    else: # default 'LAST_PIXEL':
        pad_image = np.pad(image_, ((padding_pixels, padding_pixels), (padding_pixels, padding_pixels), (0, 0)), 'edge')


    pad_image = pad_image[padding_pixels:,padding_pixels:]
    for i in range(NEW_HEIGHT):
        for j in range(NEW_WIDTH):
            x = 0
            y = 0
            if NEW_WIDTH > 1:
                x = j * (width - 1) / (NEW_WIDTH - 1)
            if NEW_HEIGHT > 1:
                y = i * (height - 1) / (NEW_HEIGHT - 1)

            x1 = int(np.floor(x))
            x2 = x1 + 1
            y1 = int(np.floor(y))
            y2 = y1 + 1

            new_image[i, j] = bi_inter(
                x1, x2, y1, y2,
                pad_image[y1, x1], pad_image[y1, x2],
                pad_image[y2, x1], pad_image[y2, x2],
                x, y
            )
    if reduce_dim:
        new_image = np.squeeze(new_image)
    return new_image