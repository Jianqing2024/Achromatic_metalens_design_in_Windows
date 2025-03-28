import numpy as np
from collections import defaultdict
import MetaSet as ms
import importlib.util
import time

spec = importlib.util.spec_from_file_location("lumapi", "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py")
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi) 

fdtd = lumapi.FDTD()
fdtd.save("fdtd_simulation.fsp")


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
                        if w <= 2 * r:
                            unclusteredParameterPet=np.vstack([unclusteredParameterPet,np.array([p,h,l,w,r])])
                            print(f"p={p} h={h} l={l} w={w} r={r}")
print("aaa间隔符")
print(unclusteredParameterPet)

print("aaa间隔符")
parameterPet = defaultdict(list)

for row in unclusteredParameterPet:
    param1, param2 = row[0], row[1]
    parameterPet[(param1, param2)].append(row)

"""
# 输出分类后的结果
for key, value in parameterPet.items():
    print(f"分类 {key}:")
    print(np.array(value))
    print()
"""

waveLength=np.linspace(0.532e-6,0.800e-6,2)

fdtd=lumapi.FDTD()
fdtd.save("fdtd_simulation.fsp")

counter=0
for key, value in parameterPet.items():
    counter+=1
    p,h=key[0],key[1]
    print(f"正在进行第{counter}次模拟, 此轮基本参数为: P={p} H={h}")
    print(value)
    for parameter in value:
        p=parameter[0] # 晶胞周期
        h=parameter[1] # 结构高度
        l=parameter[2] # 十字结构长度
        w=parameter[3] # 十字结构宽度
        r=parameter[4] # 中心圆半径
        
        for wl in waveLength:
            ms.setMetaFdtd(fdtd, p, p, 1e-6, -0.5e-6)
            ms.addMetaBase(fdtd, "SiO2 (Glass) - Palik", p, p, 0.5e-6)
            ms.addMetaSource(fdtd, p, p, -0.25e-6, wl)
            ms.classicMonitorGroup(fdtd, p, p, 1e-6)
            
            ms.addMetaRect(fdtd, "SiO2 (Glass) - Palik", l, w, h, name="recX")
            ms.addMetaRect(fdtd, "SiO2 (Glass) - Palik", w, l, h, name="recY")
            ms.addMetaCircle(fdtd, "SiO2 (Glass) - Palik", r, h)
            
            fdtd.run()
            data=ms.classicDataAcquisition(fdtd)
            
            print(data)
            
            fdtd.switchtolayout()
            fdtd.deleteall()