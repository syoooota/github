# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import glob

if __name__ == '__main__':
    img = glob.glob('../images.jpg')
    cp = Image.open(img[0]).resize((100,100))

    img = np.array(cp)
    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]
    weight = len(r[0])
    height = len(r)

    img2 = glob.glob('../hito.jpg')
    cp2 = Image.open(img2[0]).resize((100, 100))

    img2 = np.array(cp2)
    r2 = img2[:, :, 0]
    g2 = img2[:, :, 1]
    b2 = img2[:, :, 2]
    weight = len(r2[0])
    height = len(r2)

    img=(img+img2)/2
    cp = Image.fromarray(np.uint8(img))
    cp.show()