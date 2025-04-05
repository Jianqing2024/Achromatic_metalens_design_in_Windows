import numpy as np
from collections import defaultdict
from MetaSet import advancedStructure as adv
import MetaSet as ms
import importlib.util
import sqlite3
import multiprocessing

print("扫参已启动")


def simulation(wav):
    fdtd=lumapi.FDTD(hide=True)

    fdtd.save(f"s{int(wav*1e9)}.fsp")
    
    data = np.empty((0, 7))

    for key, value in parameterPet.items():
        p,h=key[0],key[1]
        ms.setMetaFdtd(fdtd, p, p, 1e-6, -0.5e-6)
        ms.classicMonitorGroup(fdtd, p, p, 1e-6)
        ms.addMetaSource(fdtd, p, p, -0.25e-6, wav)
        ms.addMetaBase(fdtd, "SiO2 (Glass) - Palik", p, p, 0.5e-6)
        for parameter in value:
            l=parameter[2] # 十字结构长度
            w=parameter[3] # 十字结构宽度
            r=parameter[4] # 中心圆半径
            
            adv.fishnetset(fdtd, "SiO2 (Glass) - Palik", h, l, w, r, name="Group")
            
            fdtd.run()
            main=np.array([p,h,l,w,r])
            da = ms.classicDataAcquisition(fdtd)
            da = np.concatenate((main, da),axis=0)
            data = np.vstack([data,da]) 
            fdtd.switchtolayout()
            fdtd.select("Group")
            fdtd.delete()

        fdtd.deleteall()
    return data

def remake(data):
    ppp=defaultdict(list)
    
    for row in data:
        param1, param2 = row[0], row[1]
        ppp[(param1, param2)].append(row)
    return ppp
 
# SQLite数据库准备
conn = sqlite3.connect("structures.db")
cursor = conn.cursor()
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

parameterPet = defaultdict(list)
    
for row in unclusteredParameterPet:
    param1, param2 = row[0], row[1]
    parameterPet[(param1, param2)].append(row)

if __name__ == "__main__":
    init = [0.532e-6, 0.800e-6]  # 输入数据
    
    with multiprocessing.Pool(processes=2) as pool:
        peta = pool.map(simulation, init)  # 将每个输入元素传给 simulation 函数并行执行
    
    data532=peta[0]
    data800=peta[1]
    data800=data800[:, -2:]
    data=np.concatenate([data532,data800],axis=1)
    
    datapet = defaultdict(list)
    
    for row in data:
        param1, param2 = row[0], row[1]
        datapet[(param1, param2)].append(row)
    
    counter=0
    for key, value in datapet.items():
        counter+=1
        baseValue=int(counter)
        for parameter in value:
            p,h,l,w,r,a532,t532,a800,t800=parameter[0],parameter[1],parameter[2],parameter[3],parameter[4],parameter[5],parameter[6],parameter[7],parameter[8]
    
            cursor.execute("""
            INSERT INTO structures (baseValue, P, H, L, W, R, angleIn532, transIn532, angleIn800, transIn800)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (baseValue, p, h, l, w, r, a532, t532, a800, t800))
            
    conn.commit()
    conn.close()