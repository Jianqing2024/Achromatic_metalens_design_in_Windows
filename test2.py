import numpy as np
from collections import defaultdict
from MetaSet import advancedStructure as adv
import MetaSet as ms
import importlib.util
import sqlite3
import multiprocessing
from tqdm import tqdm
import time
import gc

# lumapi接口准备 
spec = importlib.util.spec_from_file_location("lumapi", "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py")
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi)

P=np.linspace(0.2e-6,0.5e-6,2)
H=np.linspace(0.2e-6,0.8e-6,2)
L=np.linspace(0.04e-6,0.4e-6,2)
W=np.linspace(0.04e-6,0.4e-6,2)
R=np.linspace(0.04e-6,0.18e-6,2)

allParameterPet = np.full((0, 5), np.nan)
for p in P:
    for h in H:
        for l in L:
            if l <= p:
                for w in W:
                    for r in R:
                        if w <= 2 * r and 2 * r < p:
                            allParameterPet = np.vstack([allParameterPet, np.array([p, h, l, w, r])])


fdtd=lumapi.FDTD(hide=True)

fdtd.save(f"s{int(1)}.fsp")
    
data = np.empty((0, 9))

parameterPet=defaultdict(list)

parameterPet=defaultdict(list)
for row in allParameterPet:
    param1, param2 = row[0], row[1]
    parameterPet[(param1, param2)].append(row)
    
wav=[0.532e-6,0.800e-6]
sourceName='s'
groupName ='g'
material="SiO2 (Glass) - Palik"
    
for key, value in parameterPet.items():
    p,h=key[0],key[1]
    ms.setMetaFdtd(fdtd, p, p, 1e-6, -0.5e-6)
    ms.classicMonitorGroup(fdtd, p, p, 1e-6)
    ms.addMetaBase(fdtd, material, p, p, 0.5e-6)
    for parameter in value:
        l=parameter[2] # 十字结构长度
        w=parameter[3] # 十字结构宽度
        r=parameter[4] # 中心圆半径
            
        adv.fishnetset(fdtd, material, h, l, w, r, name=groupName)
            
        main=np.array([[p,h,l,w,r]])
            
        ms.addMetaSource(fdtd, p, p, -0.25e-6, wav[0],name=sourceName)
        fdtd.run()
        data532 = ms.classicDataAcquisition(fdtd)
        fdtd.switchtolayout()
            
        adv.swichWaveLength(fdtd, wav[1], sourceName)
        fdtd.run()
        data800 = ms.classicDataAcquisition(fdtd)
        fdtd.switchtolayout()
        
        fdtd.select(sourceName)
        fdtd.delete()
                    
        Analysis=np.concatenate((main, data532, data800),axis=1)
        data = np.concatenate((data, Analysis),axis=0)
        fdtd.select(groupName)
        fdtd.delete()


    fdtd.deleteall()
    
time.sleep(0.5)
print("Calling fdtd.close()...")
fdtd.close()
print("fdtd closed.")
gc.collect()