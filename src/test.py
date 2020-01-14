#import math
import numpy as np

size = 10
x = np.arange(size+1)
print(x, x.shape)
print(x[0])
print(x[2])
print(x[size])
print(x[1:size-1])

x.shape = (2,5)
print(x)
print(x[0:2,1])