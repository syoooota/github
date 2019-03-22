import numpy as np
import dask.array as da
import gc
cimport cython
cimport numpy as np

DTYPE = np.float32

ctypedef np.float32_t DTYPE_t

def delta_theta(np.ndarray[DTYPE_t, ndim=4] pool_map, np.ndarray[DTYPE_t, ndim=4] char_map, int fh, int fw):
                #l-1 img
    cdef int batch = len(pool_map)
    cdef int i = 0
    cdef int weight = len(pool_map[0][0])
    cdef int height = len(pool_map[0][0])
    cdef int size = weight * height
    cdef int w = weight - fw + 1
    cdef int h = height - fh + 1
    cdef int pcep = len(char_map[0])
    cdef int nxpercep = len(pool_map[0])
    cdef np.ndarray[DTYPE_t, ndim=3] a = np.reshape(char_map, (batch, pcep, -1))
    #cdef np.ndarray[DTYPE_t, ndim=3] a = np.reshape(char_map, (batch, 1, h*w))
    dth = da.from_array(a, chunks=(batch, pcep, (h*w)//2))
    cdef np.ndarray[int, ndim=1] arr = np.arange(w)  
    cdef np.ndarray[DTYPE_t, ndim=1] cmap = np.reshape(pool_map, -1)

    cdef np.ndarray[int, ndim=2] arr2 = np.reshape(np.arange(fw), (-1, 1))
    arr2 = arr + arr2
    arr2 = np.reshape(np.reshape((arr * weight),(-1, 1))+np.reshape(arr2, (fw, 1, h)), (fw, -1))
    
    cdef np.ndarray[int, ndim=3] arr3 = np.reshape(np.arange(fh),(-1, 1, 1)) * weight
    cdef np.ndarray[int, ndim=4] arr4 = np.reshape(np.arange(nxpercep), (-1, 1, 1, 1)) * size
    arr4 = arr2 + arr3 + arr4
    #a = np.reshape(cmap[arr4], (h * w, nxpercep*fw*fh))

    cdef np.ndarray[DTYPE_t, ndim=2] c = np.array([(dth[i].dot(da.from_array(np.reshape(np.take(cmap, arr4+(nxpercep*size)*i), (h * w, nxpercep*fw*fh)),\
    chunks=(h * w//2, nxpercep*fw*fh)))).compute() for i in range(batch)]).sum(0)

    
    return np.reshape(c,(pcep*nxpercep, fh, fw))




def first_delta_theta(np.ndarray[DTYPE_t, ndim=3] pool_map, np.ndarray[DTYPE_t, ndim=4] char_map, int fh, int fw):
    cdef int batch = len(pool_map)
    cdef int i = 0
    cdef int weight = len(pool_map[0][0])
    cdef int height = len(pool_map[0][0])
    cdef int size = weight * height
    cdef int w = weight - fw + 1
    cdef int h = height - fh + 1
    cdef int percep = len(char_map[0])

    #cdef np.ndarray[DTYPE_t, ndim=4] a = np.reshape(char_map, (batch, percep, 1, h * w))
    char_map = np.reshape(char_map, (batch, percep, 1, h * w))
    dth = da.from_array(char_map, chunks=(batch, percep, 1, h * w//2))
    cdef np.ndarray[int, ndim=1] arr = np.arange(w)  # [0 1...8]
    cdef np.ndarray[DTYPE_t, ndim=1] cmap = np.reshape(pool_map, -1)

    cdef np.ndarray[int, ndim=2] arr2 = np.reshape(np.arange(fw), (-1, 1))
    arr2 = arr + arr2
    arr2 = np.reshape((np.reshape((arr * weight),(-1, 1))\
     + np.reshape(arr2, (fw, 1, h))),(fw, -1))
    cdef np.ndarray[int, ndim=3] arr3 = np.reshape(np.arange(fh),(-1, 1, 1)) * weight
    #cdef np.ndarray[int, ndim=4] arr4 = np.reshape(np.arange(batch), (-1, 1, 1, 1)) * size
    arr3 = arr2 + arr3
    #cdef np.ndarray[DTYPE_t, ndim=2] c = np.reshape(cmap[arr3], (h * w, fw*fh))
    #dc = da.from_array(np.reshape(cmap[arr3], (h * w, fw*fh)), chunks=(h * w//2, fh*fw))

    pool_map = np.array([(dth[i].dot(da.from_array(np.reshape(np.take(cmap, arr3+size*i), (h * w, fw*fh)),\
    chunks=(h * w//2, fh*fw)))).compute()for i in range(batch)]).sum(0)
#    cdef np.ndarray[DTYPE_t, ndim=2] d = np.array([(cc[i:5 + i] * a[i:5 + i]).sum(-1).sum(0)\
#     for i in range(0, batch, 5)]).sum(0)

    return np.reshape(pool_map,(percep, fh, fw))

