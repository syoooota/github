# -*- coding: utf-8 -*-
from numpy import *
from numba.decorators import jit
from numba import guvectorize
import dask.array as da
import time

@jit('f4[:, :](f4[:, :], f4[:, :])')
def Total_Bakcprop(sigma, w):
    sigma = sigma.reshape(len(sigma), 1,len(sigma[0]))
    #10, 1, 20
    #w 1, 2304, 20
    x = sigma*w

    return einsum('ijk->ij', float64(x))
    #return sum(array([sigma[:, i] * w[:, i] for i in range(len(sigma[0]))])[0], axis=0)


def DropOut(unit, index):
    j = 0
    batch = len(unit)
    for j in range(batch):
        unit[j, index] = 0

    return unit

@jit('f4[:, :, :, :](f4[:, :, :, :], i8[:, :, :, :])')
def Pool_Backprop(sigmalist, index):
    i = j = k = 0
    list1 = [0]
    batch = len(index)
    percep = len(index[0])
    height = weight = len(index[0][0])
    w=weight*2
    a = zeros([batch*percep*height*2*weight*2], dtype=float)
    sig = sigmalist.reshape(-1)
    c = arange(batch*percep*height) * w
    ind = index.reshape(batch*percep*height, weight) + c.reshape(-1, 1)
    ind = ind.reshape(-1)
    ind[ind>=2]+=w-2
    for i in range(len(ind)) :
        list1.append(i*2)
    ind = ind + array(list1)[1:]
    a[ind] = sig
    return a.reshape(batch, percep, height*2, weight*2)



@jit('f8[:,:,:,:](f8[:, :, :, :])')
def differential_ReLU(x):
    x[x < 0] = 0.
    x[x > 0] = 1.
    
    return x

@jit('f4[:,:](f4[:, :], f4[:, :])')
def bindlayer_delta(unit, sigma):
    L = len(unit[0])
    batch = len(unit)
    unit = unit.reshape(batch, L, 1)
    sigma = sigma.reshape(batch, 1, -1)
    a = sum(unit*sigma, axis=0)
    return a
    
'''
@jit('f8(f8[:, :, :], f8[:, :, :], i8, i8)')
def delta_theta(pool_map, char_map, fh, fw):
                    #l-1       l
    print "p", pool_map.shape, "c", char_map.shape 
                    #例　　　32            1         20           20
    h = w = len(pool_map[0])
    pL = len(pool_map)
    cL = len(char_map)
    pm = pool_map.reshape(pL, 1, h, w)
    list1 = list2 = delta = a = array([])
    x = y = 0    
    print pm.shape
    for y in xrange(fh):
        for x in xrange(fw):
            a = pm[:, :, y:h-fh+y+1, x:w-fw+x+1]*char_map[:]
            a = vstack((a))
            a = sum(sum(a, axis=1), axis=1).reshape(-1, 1)
            if(x==0):
                list1 = a
            else:
                list1 = hstack((list1, a))
        if(y==0):
            list2 = list1
        else:
            list2 = hstack((list2, list1))
        
    delta = list2.reshape(pL*cL, fh, fw)
    print delta.shape
    return delta            
'''


def delta_theta(pool_map, char_map, fh, fw):
    # l-1 img       l
    batch = len(pool_map)
    weight = len(pool_map[0][0])
    height = len(pool_map[0][0])
    size = weight * height
    w = weight - fw + 1
    h = height - fh + 1
    percep = len(char_map[0])
    nxpercep = len(pool_map[0])
    a = reshape(char_map, (batch, 1, percep, 1, h * w))
    print (a.shape)
    dth = da.from_array(a, chunks=(batch // 2, 1, percep // 2, 1, h * w))

    arr =arange(w)  # [0 1...8]
    cmap = reshape(pool_map, -1)
    arr2 = reshape(arange(fw), (-1, 1))
    x = arr + arr2
    xy = reshape((reshape((arr * weight), (-1, 1)) + reshape(x, (fw, 1, h))), (fw, -1))

    st = time.time()
    arr3 = reshape(arange(fh), (-1, 1, 1)) * weight
    arr4 = reshape(arange(batch * nxpercep), (-1, 1, 1, 1)) * size
    xyz = xy + arr3 + arr4
    c = cmap[xyz]
    print (c.shape)
    elapsed_time = time.time() - st
    print("elapsed_time:{0}".format(elapsed_time))

    st = time.time()
    cc = reshape(c, (batch, nxpercep, 1, fw * fh, h * w))  # * theta
    dc = da.from_array(cc, chunks=(batch // 2, nxpercep // 2, 1, fh * fw, h * w))
    d = array([(dc[i:5 + i] * dth[i:5 + i]).sum(-1).sum(0).compute() \
                  for i in range(0, batch, 5)]).sum(0)
    print(d.shape)
    elapsed_time = time.time() - st
    print("elapsed_time:{0}".format(elapsed_time))
    return d.reshape(percep * nxpercep, fh, fw)



@jit('f4(f4[:, :, :], f4[:, :, :, :], i8, i8)')
def first_delta_theta(pool_map, char_map, fh, fw):
    x=y=0
    cL = len(char_map[0])
    #L1=len(char_map)
    batch = len(pool_map)
    h = w = len(pool_map[0])
    pool_map = pool_map.reshape(batch, 1, h, w)
    print ("p", pool_map.shape, "c", char_map.shape) 
    a=list1=list2=array([])
    for y in range(fh):
        for x in range(fw):
            a=pool_map[:, :, y:100-fh+y+1, x:100-fw+x+1]*char_map
            a=einsum('ijkl->j', a).reshape(cL, 1, 1)
            #a=array(sum(sum(sum(, axis=0), axis=1), axis=1)).reshape(-1, 1)
            if(x==0):
                list1 = a
            else:
                list1 = concatenate((list1, a), axis=-1)
        if(y==0):
            list2 = list1
        else:
            list2 = concatenate((list2, list1), axis=-2)

    return list2


@jit('f4[:](f4[:, :, :, :])')
def delta_bias(char_map):
    return einsum('ijkl->j', char_map)
    #return sum(sum(sum(char_map, axis=0), axis=1), axis=1).reshape(-1)


@jit
def Gradient_Descent(delta, theta, alfa, batch):                    
    theta = theta - alfa*((1/batch)*delta)
    return theta


def diff_Maxout(x, ind):
    batch, maps, mx, my=x.shape
    
    a=x.reshape(-1)
    mxy = mx * my
    a = x.reshape(-1)
    arr = arange(batch * maps) * mxy
    arr2 = arange(len(a))
    b = zeros(len(a) * 2)
    ind = where(ind == 1)
    arr2[ind] += mxy
    arr2 = arr2.reshape(-1, mxy) + arr.reshape(-1, 1)
    b[arr2] = a
    
    return array(b).reshape(batch, maps*2, mx, my)


def diff_Maxout2(x, ind, num):
    batch, maps, mx, my=x.shape
    x = x.reshape(-1)
    mxy = mx * mx
    a = len(x)
    z = zeros((num, a))    
    ind = ind.reshape(-1)
    for i in range(a):
        z[ind[i], i] = x[i] 
    
    z = array(hsplit(z, batch*maps))
    
    return z.reshape(batch, maps*num, mx, my)

def diff_Minout(x, ind):
    batch, maps, mx, my=x.shape
    
    a=x.reshape(-1)
    mxy = mx * my
    arr = arange(batch * maps) * mxy
    arr2 = arange(len(a))
    b = zeros(len(a) * 2)
    ind = where(ind == 1)
    arr2[ind] += mxy
    arr2 = arr2.reshape(-1, mxy) + arr.reshape(-1, 1)
    b[arr2] = a
    
    return array(b).reshape(batch, maps*2, mx, my)


def diff_Drop(x, ind):
    i = j =0
    batch = len(unit)
    L = len(unit[0])
    
    for j in range(batch):
        unit[j, index] = 0
        
    return unit

def diff_sort(x, ind):
    
    batch = len(x)
    z = zeros((batch, len(x[0])))
    for i in range(batch):
        for j in range(len(x[0])):
            z[i, ind[i, j]] = x[i, j]
            
    return z
