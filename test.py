import multiprocessing
from MetaSet import advancedStructure as ad
import numpy as np
from time import time

def computer(z):
    tic=time()
    num=str(int(z[0]*1e9))
    meta=ad.MetaEngine(name=num)
    meta.materialSet()
    meta.baseBuild(0.4e-6)
    for r in z:
        pa=[r]
        meta.structureBuild(1, pa, 0.6e-6)
        meta.dataAcquisition()
        print(f'{meta.Ex}|{meta.Trans}')
        meta.semi_Reset()
        
    meta.fdtd.close()
    toc=time()
    print(f'{toc-tic}s')
    return 'a'

def main(parallelsNum, parameter):
    processes = []

    for i in range(parallelsNum):
        iterations = parameter[i]
        p = multiprocessing.Process(target=computer, args=(iterations,))
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    print("所有进程已完成")

if __name__ == '__main__':
    
    z1=np.linspace(0.01e-6,0.1e-6,5)
    z2=np.linspace(0.02e-6,0.2e-6,5)
    z3=np.linspace(0.03e-6,0.1e-6,5)
    z4=np.linspace(0.04e-6,0.2e-6,5)
    parameter=[z1,z2,z3,z4]
    
    tic=time()
    aaa=main(4,parameter)
    toc=time()
    print(f'first{toc-tic}s')
    
    tic=time()
    for z in parameter:
        computer(z)
        
    toc=time()
    print(f'second{toc-tic}s')