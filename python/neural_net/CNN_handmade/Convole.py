# -*- coding: utf-8 -*-
from numpy import *
from numba.decorators import jit
import dask.array as da
import time


@jit
def ImageProcessing1(img, fw, fh, weight, height, theta):
   pcep=len(theta)
   batch=len(img)
   size = weight * height
   w = weight - fw + 1
   h = height - fh + 1
   i = 0
   theta = theta.reshape(pcep, fh* fw, 1)
   im=img.reshape(-1)
   arr = arange(fw) # [0 1...8]
   arr2 = arange(w).reshape(-1, 1)
   arr2 = (((arr*weight).reshape(-1, 1))\
           +(arr+arr2).reshape(w, 1, fh)).reshape(w, -1)

   arr3 = ((arange(h)).reshape(-1, 1, 1)) * weight
   arr4 = (arange(batch).reshape(-1, 1, 1, 1)) * size

   arr4 = arr2 + arr4 + arr3
   c = im[arr4]
   del arr4
   c = c.reshape(batch, 1, h* w,fh*fw)

   c=array([c[i].dot(theta)for i in range(batch)])
   
   return c.reshape(batch, pcep, h, w)


# @jit('f4[:, :, :, :](f4[:, :, :, :], i8, i8, i8, i8, f4[:, :, :], i8, i8)')
def ImageProcessing2(char_map, fw, fh, weight, height, theta, percep, nxpercep):

   batch=len(char_map)
   #pcep = len(theta)
   size = weight * height
   h = w = weight - fw + 1
   th = theta.reshape(percep, nxpercep, 1, fh*fw)
   #dth = da.from_array(theta, chunks=(percep // 2, nxpercep//2, 1, fh * fw))
   arr = arange(fw).astype(int)  # [0 1...8]
   #li = ones((batch * pcep, h, 1, 1), int)
   char_map = char_map.reshape(-1)

   arr2 = arange(w).reshape(-1, 1)
   x = arr + arr2
   xy = (arr * weight).reshape(-1, 1) + x.reshape(w, 1, fh)
   xy = xy.reshape(w, -1)


   # print (xy.shape)
   st = time.time()
   arr = arange(h).reshape(-1, 1, 1) * weight
   arr2 = arange(batch * percep).reshape(-1, 1, 1, 1) * size
   xy = xy + arr + arr2
   print (xy.shape)
   c = char_map[xy]
   #del xy, arr2, arr, x
   #gc.collect()
   elapsed_time = time.time() - st
   print("elapsed_time:{0}".format(elapsed_time))

   st = time.time()
   c = c.reshape(batch, percep, 1, h*w, fh*fw)  # * theta
   #dc = da.from_array(c, chunks=(batch//2, percep // 2, 1, h*w, fh*fw))
   c = (c*th).sum(axis=-1).sum(axis=1)                           #freeze float64
   '''
   c=[0]
   for i in range(0, batch, 5):
      c.append((dc[i:5 + i] * dth).sum(-1).sum(1).compute())
   '''
   #c=array([(c[i:5+i]*th).sum(-1).sum(1).compute() for i in range(0, batch, 5)])

   elapsed_time = time.time() - st
   print("elapsed_time:{0}".format(elapsed_time))
   print (c.shape)
   return c.reshape(batch, nxpercep, h, w)


@jit('f8(f8[:, :, :, :], i8, i8, i8, i8)')
def Pooling(char_map, weight, height, percep, fsize):
   size = weight * height
   h = w = weight//fsize
   batch = len(char_map)
   arr = arange(weight)  # [0 1...8]

   img = char_map.reshape(-1)

   #arr2 = arange(0, weight, 2).reshape(-1, 1)
   x = arr.reshape(w, fsize)
   arr2=x+weight
   xy=hstack((x,arr2))
   #xy = (arr * weight).reshape(-1, 1) + x.reshape(w, 1, 2)
   #xy = xy.reshape(w, -1)

   arr = arange(0, height, fsize).reshape(-1, 1, 1) * weight
   arr2 = arange(batch*percep).reshape(-1, 1, 1, 1) * size

   xy = xy + arr + arr2
   # print (xy.shape)
   c = img[xy]
   c = c.reshape(batch, percep, h, w, fsize*2)

   pool = c.max(axis=-1)
   index = c.argmax(-1)

   return (pool, index)


def Pool2(img,  weight, height, pcep, size):
   fw=fh=size
   batch=len(img)
   size = weight * height
   w = weight - fw + 1
   h = height - fh + 1
   i = 0
   
   im=img.reshape(-1)
   arr = arange(fw) # [0 1...8]
   arr2 = arange(w).reshape(-1, 1)
   arr2 = (((arr*weight).reshape(-1, 1))\
           +(arr+arr2).reshape(w, 1, fh)).reshape(w, -1)

   arr3 = ((arange(h)).reshape(-1, 1, 1)) * weight
   arr4 = (arange(batch).reshape(-1, 1, 1, 1)) * size

   arr4 = arr2 + arr4 + arr3
   c = im[arr4]
   del arr4
   c = c.reshape(batch, 1, h* w,fh*fw)
   
   index = c.argmax(-1)
   c = c.max(axis=-1)
   
   return c.reshape(batch, pcep, h, w)



@jit('f8[:, :, :, :](f8[:, :, :, :], i8, i8, i8, i8)')
def mean_pl(char_map, weight, height, percep, fsize):
   size = weight * height
   h = w = weight//fsize
   batch = len(char_map)
   arr = arange(weight)  # [0 1...8]

   img = char_map.reshape(-1)

   #arr2 = arange(0, weight, 2).reshape(-1, 1)
   x = arr.reshape(w, fsize)
   arr2=x+weight
   xy=hstack((x,arr2))
   #xy = (arr * weight).reshape(-1, 1) + x.reshape(w, 1, 2)
   #xy = xy.reshape(w, -1)

   arr = arange(0, height, fsize).reshape(-1, 1, 1) * weight
   arr2 = arange(batch*percep).reshape(-1, 1, 1, 1) * size

   xy = xy + arr + arr2
   # print (xy.shape)
   c = img[xy]
   c = c.reshape(batch, percep, h, w, fsize*2)
   pool = c.sum(-1)/(fsize*2)
   
   return pool



def Initialization(fh, fw, fn):
   num = random.rand(fn)
   b = []
    
   for i in range(fn):
      a = random.rand(fh, fw)*(2*num[i])-num[i]
      b.append(a)
      theta=array(b)
      
   return theta

@jit('f4[:, :, :, :](f4[:, :, :, :])')
def ReLU (x):
   #a,b,c,d=x.shape
   #e = x.reshape(-1)
   x[x<0] = 0
   return x
   #return e.reshape(a, b, c, d).astype(float32)

#@jit('f4[:, :, :, :](f4[:, :, :, :], i8)')
def Pading (x, num):
   
   dsize = ndim(x)
   li = [x.shape[i] for i in range(dsize)]
   li[-1] = li[-1] + num*2
   li[-2] = li[-2] + num*2
   
   a = zeros(li).reshape(-1, li[dsize-2], li[dsize-1])
   x = x.reshape(-1, size(x, -2), size(x, -1))
   a[:, num:li[dsize-2]-num, num:li[dsize-1]-num] = x
   
   return a.reshape(li)
   
   
def Maxout(x):
   batch, maps, mx, my=x.shape
   a = x.reshape(-1)
   mxy = mx*my
   arr2=arange(len(a)).reshape(-1, mxy)
   arr2=array(split(arr2, batch*maps//2, axis=0)).transpose(0, 2, 1)
   arr2=a[arr2]
   arr3=arr2.max(-1)
   index=arr2.argmax(-1).reshape(-1)
   
   return (array(arr3).reshape(batch, maps//2, mx, my), array(index))


def Maxout2(x, num):
   batch, maps, mx, my=x.shape
   a = x.reshape(-1)
   mxy = mx*my
   arr2=arange(len(a)).reshape(-1, mxy)
   arr2=array(split(arr2, batch*maps//num, axis=0)).transpose(0, 2, 1)
   arr2=a[arr2]
   arr3=arr2.max(-1)
   index=arr2.argmax(-1).reshape(-1)
   
   return (array(arr3).reshape(batch, maps//num, mx, my), array(index))


def Minout(x):
   batch, maps, mx, my=x.shape
   a = x.reshape(-1)
   mxy = mx*my
   arr2=arange(len(a)).reshape(-1, mxy)
   arr2=array(split(arr2, batch*maps//2, axis=0)).transpose(0, 2, 1)
   arr2=a[arr2]
   arr3=arr2.min(-1)
   index=arr2.argmin(-1).reshape(-1)
   
   return (array(arr3).reshape(batch, maps//2, mx, my), array(index))


def step(x):
   x[x > 0] = 1      #１　逆順だめ
   x[x < 0] = 0      #2
   
   return x


@jit('f8[:, :](f8[:])')
def sigmoid(x):
   gain=0.001
   #gain=1
   
   #dsize = ndim(x)
   #li = [x.shape[i] for i in range(dsize)]   
 
   
   x[(isnan(x)) | (x<(-708/gain))]=-708/gain
   x[(isinf(x)) | (x>(708)/gain)]=709/gain
   z = exp(x*gain)
   x = z / (1.0 + z)   
   
   
   
   x[x>0.99999]=0.99999
   x[x<0.00001]=0.00001
   return x

def mytanh(x):
   gain = 0.01
   a = tanh(x*gain)
   
   a[a < -0.9999] = -0.9999
   a[a > 0.9999] = 0.9999
   
   return a