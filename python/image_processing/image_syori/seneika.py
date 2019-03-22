# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import glob

if __name__ == '__main__':
    img = glob.glob('../median_kinkaku.jpg')
    cp = Image.open(img[0])

    img = np.array(cp)
    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]

    fl = np.array([[-1,-1,-1],
                   [-1,16,-1],
                   [-1,-1,-1]])/8
    '''

    fl = np.array([[0, -1, 0],
                   [-1, 5, -1],
                   [0, -1, 0]])
    '''

    weight = len(r[0])
    height = len(r)
    r = np.reshape(r, (height, weight))
    g = np.reshape(g, (height, weight))
    b = np.reshape(b, (height, weight))
    for k in range(height - 3 + 1):
        for j in range(weight - 3 + 1):
            aa = (r[k:k + 3, j:j + 3] * fl).sum().astype(int)
            bb = (g[k:k + 3, j:j + 3] * fl).sum().astype(int)
            cc = (b[k:k + 3, j:j + 3] * fl).sum().astype(int)
            cp.putpixel((j + 1, k + 1), (aa, bb, cc))
    cp.save('../kinkaku3.jpg')
