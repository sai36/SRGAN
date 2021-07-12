from numba import jit, cuda, vectorize
import numpy as np
# to measure exec time
from timeit import default_timer as timer   
  
# normal function to run on cpu
@vectorize(['float64(float64)'], target ="cuda")
def func(a):                                
    for i in range(10000000):
        a[i]+= 1      
  
# function optimized to run on gpu 
#@jit(target ="cuda")                         
@vectorize(['float64(float64)'], target ="cuda")
def func2(a):
    return a+1

if __name__=="__main__": 
    n = 10000000                            
    a = np.ones(n, dtype = np.float64) 

    start = timer() 
    func(a) 
    print("without GPU:", timer()-start)     

    start = timer() 
    func2(a) 
    print("with GPU:", timer()-start) 
'''      
    start = timer()
    func2(a)
    print("with GPU:", timer()-start)
'''
