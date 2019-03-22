# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import glob

if __name__ == '__main__':
    img = glob.glob('../kinkaku3.jpg')
    cp = Image.open(img[0])

    img = np.array(cp)
    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]
    weight = len(r[0])
    height = len(r)
    aa=np.copy(r)
    bb=np.copy(g)
    cc=np.copy(b)

    min_table = 30
    max_table = 200
    diff_table = max_table - min_table
    ganma = 2

    for i in range(0, min_table):
        r[aa==i] = 0
        g[bb==i] = 0
        b[cc==i] = 0

    for i in range(min_table, max_table):
        src = i
        dst = 255 * (i - min_table) / diff_table
        r[aa==i]=dst
        g[bb==i]=dst
        b[cc==i]=dst

    for i in range(max_table, 255):
        r[aa==i] = 255
        g[bb==i] = 255
        b[cc==i] = 255

    cp = Image.fromarray(np.uint8(img))
    cp.save('../kinkaku2.jpg')

        #print((r==188).shape)
