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
    
    img[:, :, 0]=bb
    img[:, :, 1]=aa
    img[:, :, 2]=aa
    
    cp = Image.fromarray(np.uint8(img))
    cp.save('../kinkaku7.jpg')    