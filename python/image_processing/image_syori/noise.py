# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import glob
import random


if __name__ == '__main__':
    sio_num = 1000


    img = glob.glob('../kinkaku.jpg')
    cp = Image.open(img[0])


    img = np.array(cp)
    r = img[:, :, 0]
    g = img[:, :, 1].reshape(-1)
    b = img[:, :, 2].reshape(-1)
    weight = len(r[0])
    height = len(r)
    r=r.reshape(-1)
    if sio_num > weight*height:
        print("error")
        exit()

    num = np.arange(weight*height).tolist()
    sio = random.sample(num, sio_num)
    r[sio]=255
    g[sio]=255
    b[sio]=255
    cp = Image.fromarray(np.uint8(img))

    cp.save('../sio_kinkaku.jpg')

