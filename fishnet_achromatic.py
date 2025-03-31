import numpy as np
from collections import defaultdict
from MetaSet import advancedStructure as adv
import MetaSet as ms
import importlib.util
import sqlite3
import time

# lumapi接口准备 
spec = importlib.util.spec_from_file_location("lumapi", "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py")
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi) 

# SQLite数据库准备
conn = sqlite3.connect("structures.db")
cursor = conn.cursor()
# 重置数据库
cursor.execute("DELETE FROM structures;")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='structures';")

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

# 模拟准备   
fdtd=lumapi.FDTD()
fdtd.save("simulation.fsp")
# fdtd=lumapi.FDTD(filename='simulation.fsp',hide=False)

ms.setMetaFdtd(fdtd, p, p, 1e-6, -0.5e-6)
ms.classicMonitorGroup(fdtd, p, p, 1e-6)

# 计算并录入数据
counter=0
waveLength=np.linspace(0.532e-6,0.800e-6,2)
start_time = time.time()
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
        
        ms.addMetaBase(fdtd, "SiO2 (Glass) - Palik", p, p, 0.5e-6)
        
        data = np.zeros(4)
        for i, wl in enumerate(waveLength):
            ms.addMetaSource(fdtd, p, p, -0.25e-6, wl)
            adv.fishnetset(fdtd, "SiO2 (Glass) - Palik", h, l, w, r, name="Group")

            fdtd.run()
            temporaryValue = ms.classicDataAcquisition(fdtd)

            data[i * 2], data[i * 2 + 1] = temporaryValue  # 直接按索引存储

            print("本次运算已完成")

            fdtd.switchtolayout()
            fdtd.select("Group")
            fdtd.delete()
            fdtd.select("source")
            fdtd.delete()

        cursor.execute("""
        INSERT INTO structures (baseValue, P, H, L, W, R, angleIn532, transIn532, angleIn800, transIn800)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (int(counter), p, h, l, w, r, data[0], data[1], data[2], data[3]))

"""
以后要改为只存入一次数据,减少i/o消耗
想办法可以改参数而不是删结构，但我觉得其实差不多
再确认一次参数选择的规则

可以招出两个fdtd区域后,一个专门处理532,一个专门处理800.这样的话虽然只有两重并行,但不需要反复招出fdtd窗口,而且需要删除的结构又少了一个
"""


conn.commit()
conn.close()    
                    
end_time = time.time()
execution_time = end_time - start_time
print(f"运算时间: {execution_time} 秒")