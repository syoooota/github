# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
from PIL import ImageEnhance
import glob

if __name__ == '__main__':
    img = glob.glob('../kinkaku4.jpg')
    img = Image.open(img[0])

    #img = np.array(img)*1.5
    bright = ImageEnhance.Brightness(img).enhance(1.3)
    
    #sharp = ImageEnhance.Sharpness(bright).enhance(0.01) 

    #img.point(lambda x: x*5)
    '''
    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]
    weight = len(r[0])
    height = len(r)
    aa=np.copy(r)
    bb=np.copy(g)
    cc=np.copy(b)
    '''
    
    #cp = Image.fromarray(np.uint8(img))
    bright.save('../kinkaku5.jpg')  
    #img.save('../kinkaku5.jpg')    