# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np
import glob

if __name__ == '__main__':
    img = glob.glob('../sio_kinkaku.jpg')
    cp = np.array(Image.open(img[0]))
    #フィルターサイズ
    f=3

    img = np.copy(cp)

    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]
    weight = len(r[0])
    height = len(r)

    for i in range(weight-f-1):
        for j in range(height-f-1):
            if r[j+1,i+1]>=230 or g[j+1,i+1]>=230 or b[j+1,i+1]>=230:
                cp[j+1, i+1, 0]=np.median(r[j:j+f, i:i+f])
                cp[j + 1, i + 1, 1] = np.median(g[j:j + f, i:i + f])
                cp[j + 1, i + 1, 2] = np.median(b[j:j + f, i:i + f])

    cp = Image.fromarray(np.uint8(cp))
    cp.save('../median_kinkaku.jpg')
