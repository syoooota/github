# -*- coding: utf-8 -*-
from numpy import *
from numba.decorators import jit
from numba import guvectorize
import math


def TotalBindingInit(unitsize, outlayer):
        num = random.rand()
        w = random.rand(unitsize, outlayer)*(2*num)-num
        return array(w)
 
'''      
@jit('f8(f8[:], f8[:])')
def TotalBindingProcess(unit, w):
        i = 0
        a = array([])
        L = len(unit)
        for i in range(L):
                if(i==0):
                        a = array(unit[i] * w[i])
                else:
                        b = array(unit[i] * w[i])
                        a = a + b
        return a
'''
@jit('f4[:,:](f4[:,:,:], f4[:,:])')
def TotalBindingProcess(unit, w):
        return sum(unit*w, axis=1)


@jit('f8[:, :, :, :](f8[:, :], f4[:,:])')
def DropOut(unit, rate):
        j =0
        batch = len(unit)
        L = len(unit[0])
        #x = random.binomial(n=L, p=0.5)
        
        #for i in index:
        index = [0]
        for j in range(batch):
                num = random.choice(range(L), int(L*rate), replace=False)
                unit[j, num] = 0.0
                
                index.append(num)
        index = index[1:]
        
        return (unit,array(index))

@jit('f8[:, :](f8[:, :], int8[:,:])')
def diff_Drop(unit, index):
        j =0
        batch = len(unit)
        #x = random.binomial(n=L, p=0.5)
        
        #for i in index:
        for j in range(batch):
                unit[j, index[j]] = 0.0
                
        return unit.reshape(batch, -1, 1)


   
@jit('f8[:, :](f8[:])')
def sigmoid(x):
        gain=0.01
        #dsize = ndim(x)
        #li = [x.shape[i] for i in range(dsize)]   


        x[(isnan(x)) | (x<-708)]=-708
        x[(isinf(x)) | (x>708)]=709
        z = exp(x*gain)
        x = z / (1.0 + z)   



        x[x>0.9999]=0.9999
        x[x<0.0001]=0.0001   
        return x


@jit('f8[:, :, :,:](f8[:, :], i8)')
def Maxout(x, num):
        batch = len(x)
        x = x.reshape(batch, -1, num)
        ind = x.argmax(-1)
        x = x.max(-1)
        return (x, ind)

@jit('f8[:, :](f8[:, :], f8[:, :], i8)')
def difMax(x, ind, num):
        batch = len(x)
        L = len(x[0])
        x = x.reshape(-1)
        z = zeros((batch*L,num))
        ind = ind.reshape(-1)
        for i in range(batch*L):
                z[i, ind[i]] = x[i]
        #arr = arr.reshape(-1, 1)
        
        return z.reshape(batch, -1, 1)