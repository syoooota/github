# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import glob

if __name__ == '__main__':
    img = glob.glob('../kinkaku.jpg')
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

    ganma = 0.7


    for i in range(1, 255):
        dst = ((i/255)**(1/ganma))*255
        r[aa==i]=dst
        g[bb==i]=dst
        b[cc==i]=dst

    cp = Image.fromarray(np.uint8(img))
    cp.save('../kinkaku3.jpg')

        #print((r==188).shape)