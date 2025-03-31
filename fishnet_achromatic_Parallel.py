import numpy as np
from collections import defaultdict
from MetaSet import advancedStructure as adv
import MetaSet as ms
import importlib.util
import sqlite3
import time
import multiprocessing

def simulation(wav):
    if wav==0.532e-6:
        fdtd1=lumapi.FDTD()
        fdtd=fdtd1
    elif wav==0.800e-6:
        fdtd2=lumapi.FDTD()
        fdtd=fdtd2
    
    fdtd.save("simulation.fsp")
    
    data = np.empty((0, 2))

    for key, value in parameterPet.items():
        p,h=key[0],key[1]
        print(value)
        ms.setMetaFdtd(fdtd, p, p, 1e-6, -0.5e-6)
        ms.classicMonitorGroup(fdtd, p, p, 1e-6)
        ms.addMetaSource(fdtd, p, p, -0.25e-6, wav)
        ms.addMetaBase(fdtd, "SiO2 (Glass) - Palik", p, p, 0.5e-6)
        
        for parameter in value:
            p=parameter[0] # 晶胞周期
            h=parameter[1] # 结构高度
            l=parameter[2] # 十字结构长度
            w=parameter[3] # 十字结构宽度
            r=parameter[4] # 中心圆半径
            
            adv.fishnetset(fdtd, "SiO2 (Glass) - Palik", h, l, w, r, name="Group")
            
            fdtd.run()
            da = ms.classicDataAcquisition(fdtd)
            data = np.vstack([data, da]) 

            print("本次运算已完成")

            fdtd.switchtolayout()
            fdtd.select("Group")
            fdtd.delete()
            
        fdtd.deleteall()
    
    
    return data

#"SiO2 (Glass) - Palik"
# lumapi接口准备 
spec = importlib.util.spec_from_file_location("lumapi", "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py")
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi) 

# 计算参数
P=np.linspace(0.2e-6,0.5e-6,2)
H=np.linspace(0.2e-6,0.8e-6,2)
L=np.linspace(0.04e-6,0.4e-6,2)
W=np.linspace(0.04e-6,0.4e-6,2)
R=np.linspace(0.04e-6,0.18e-6,2)

unclusteredParameterPet = np.full((0, 5), np.nan)
for p in P:
    for h in H:
        for l in L:
            if l <= p:
                for w in W:
                    for r in R:
                        if w <= 2 * r and 2 * r < p:
                            unclusteredParameterPet = np.vstack([unclusteredParameterPet, np.array([p, h, l, w, r])])
                            print(f"p={p} h={h} l={l} w={w} r={r}")

parameterPet = defaultdict(list)
    
for row in unclusteredParameterPet:
    param1, param2 = row[0], row[1]
    parameterPet[(param1, param2)].append(row)


data=simulation(0.532e-6)
print(data)
