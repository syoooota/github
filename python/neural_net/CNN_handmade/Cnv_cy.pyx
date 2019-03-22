import numpy as np
import dask.array as da
import gc
cimport cython
cimport numpy as np

DTYPE = np.float32
ctypedef np.float32_t DTYPE_t

def ImageProcessing1(np.ndarray[DTYPE_t, ndim=3] img, int fw, int fh, int weight, int height,\
 np.ndarray[DTYPE_t, ndim=3] theta):
   
   cdef int pcep=len(theta)
   cdef int batch=len(img)
   cdef int size = weight * height
   cdef int w = weight - fw + 1
   cdef int h = height - fh + 1
   cdef int i = 0
   theta = np.reshape(theta, (pcep, 1,  fh* fw))
   #theta = np.reshape(theta, (pcep, fh* fw, 1)
   #dth=da.from_array(theta, chunks=(pcep//2, 1, fh*fw,))
   #dth=da.from_array(theta, chunks=(pcep//2, fh*fw, 1))
   cdef np.ndarray[DTYPE_t, ndim=1] im=np.reshape(img, -1)
   cdef np.ndarray[int, ndim=1] arr = np.arange(fw) # [0 1...8]
   cdef np.ndarray[int, ndim=2] arr2 = np.reshape(np.arange(w),(-1, 1))
   arr2 = np.reshape((np.reshape((arr*weight), (-1, 1))\
   +np.reshape(arr+arr2, (w, 1, fh))), (w, -1))

   cdef np.ndarray[int, ndim=3] arr3 = np.reshape((np.arange(h)),(-1, 1, 1)) * weight
   cdef np.ndarray[int, ndim=4] arr4 = np.reshape(np.arange(batch), (-1, 1, 1, 1)) * size

   arr3 = arr2  + arr3
   
   cdef np.ndarray[DTYPE_t, ndim=4] d=np.array([theta.dot(np.reshape(np.take(im, arr3+size*i),(fh*fw, h* w)))for i in range(batch)])
   #cdef np.ndarray[DTYPE_t, ndim=3] d=(img[arr4]*theta).sum(-1)

   return np.reshape(d,(batch, pcep, h, w))



def ImageProcessing2(np.ndarray[DTYPE_t, ndim=4] char_map, int fw, int fh, \
int weight, int height, np.ndarray[DTYPE_t, ndim=3] theta, int nxpcep):

   cdef int pcep=len(char_map[0])
   #cdef int nxpcep=len(theta)
   cdef int batch=len(char_map)
   cdef int size = weight * height
   cdef int w = weight - fw + 1
   cdef int h = height - fh + 1
   cdef int i = 0
   cdef np.ndarray[DTYPE_t, ndim=2] th = np.reshape(theta,(nxpcep, -1))
   dth = da.from_array(th, chunks=(nxpcep, pcep*fh * fw//2))
   cdef np.ndarray[DTYPE_t, ndim=1] cmap = np.reshape(char_map, (-1))
   cdef np.ndarray[int, ndim=1] arr = np.arange(fw) # [0 1...8]
   cdef np.ndarray[int, ndim=2] arr2 = np.reshape(np.arange(w),(-1, 1))
   arr2 = np.reshape((np.reshape((arr*weight), (-1, 1))\
   +np.reshape(arr+arr2, (w, 1, fh))), (w, -1))

   cdef np.ndarray[int, ndim=3] arr3 = np.reshape((np.arange(h)),(-1, 1, 1)) * weight
   cdef np.ndarray[int, ndim=4] arr4 = np.reshape(np.arange(pcep), (-1, 1, 1, 1)) * size

   arr4 = arr2 + arr4 + arr3

   #cdef np.ndarray[DTYPE_t, ndim=2] c = np.reshape(cmap[arr4],(pcep*fh*fw, h*w))
   cdef np.ndarray[DTYPE_t, ndim=3] c=np.array([(dth.dot(da.from_array(np.reshape(np.take(cmap, arr4+(pcep*size)*i),(pcep*fh*fw, h*w)), \
   chunks=(fh*fw*pcep // 2, h*w)))).compute() for i in range(batch)])
   #print(d.shape)   
#   cdef np.ndarray[DTYPE_t, ndim=4] d=np.array([(cc[i:5+i]*th).sum(-1).sum(1) for i in range(0, batch, 5)])

   return np.reshape(c, (batch, nxpcep, h, w))


def ImageProcessing3(np.ndarray[DTYPE_t, ndim=4] char_map, int fw, int fh, \
int weight, int height, np.ndarray[DTYPE_t, ndim=3] theta):

   cdef int pcep=len(theta)
   cdef int batch=len(char_map)
   cdef int size = weight * height
   cdef int w = weight - fw + 1
   cdef int h = height - fh + 1
   cdef int i = 0
   cdef np.ndarray[DTYPE_t, ndim=1] th = np.reshape(theta,(-1))
   dth = da.from_array(th, chunks=(pcep*fh * fw//2))
   cdef np.ndarray[DTYPE_t, ndim=1] cmap = np.reshape(char_map, (-1))
   cdef np.ndarray[int, ndim=1] arr = np.arange(fw) # [0 1...8]
   cdef np.ndarray[int, ndim=2] arr2 = np.reshape(np.arange(w),(-1, 1))
   arr2 = np.reshape((np.reshape((arr*weight), (-1, 1))\
   +np.reshape(arr+arr2, (w, 1, fh))), (w, -1))

   cdef np.ndarray[int, ndim=3] arr3 = np.reshape((np.arange(h)),(-1, 1, 1)) * weight
   cdef np.ndarray[int, ndim=4] arr4 = np.reshape(np.arange(pcep), (-1, 1, 1, 1)) * size

   arr4 = arr2 + arr4 + arr3

   #cdef np.ndarray[DTYPE_t, ndim=2] c = np.reshape(cmap[arr4],(pcep*fh*fw, h*w))
   cdef np.ndarray[DTYPE_t, ndim=2] c=np.array([(dth.dot(da.from_array(np.reshape(np.take(cmap, arr4+(pcep*size)*i),(pcep*fh*fw, h*w)), \
   chunks=(fh*fw*pcep // 2, h*w//2)))).compute() for i in range(batch)])
   #print(d.shape)   
#   cdef np.ndarray[DTYPE_t, ndim=4] d=np.array([(cc[i:5+i]*th).sum(-1).sum(1) for i in range(0, batch, 5)])

   return np.reshape(c, (batch,  h, w))
