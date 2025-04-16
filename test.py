import numpy as np
from collections import defaultdict
from MetaSet import advancedStructure as adv
import MetaSet as ms
import importlib.util
import sqlite3
import multiprocessing
from tqdm import tqdm

# lumapi接口准备 
spec = importlib.util.spec_from_file_location("lumapi", "D:\\Program Files\\Lumerical\\v241\\api\\python\\lumapi.py")
lumapi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lumapi)

def split_matrix(matrix,num):
    n, m = matrix.shape
    # 平均行数，向下取整
    avg_rows = n // num
    remainder = n % num

    # 每份的行数
    part_sizes = [avg_rows] * num
    for i in range(remainder):
        part_sizes[i] += 1  # 尽量平均地把余数分给前面几份

    # 为了让第四份最小，把多余的行尽量分配给前3份
    if remainder:
        # 把最后一份的行数向前移动
        for i in range(3, 0, -1):
            while part_sizes[3] > avg_rows and part_sizes[i-1] < avg_rows + 1:
                part_sizes[3] -= 1
                part_sizes[i-1] += 1

    # 根据行数分割
    parts = []
    start = 0
    for size in part_sizes:
        parts.append(matrix[start:start+size])
        start += size

    return parts

def simulation(parameter,part):
    
    fdtd=lumapi.FDTD(hide=True)

    fdtd.save(f"s{int(part)}.fsp")
    
    data = np.empty((0, 9))

    parameterPet=defaultdict(list)
    for row in parameter:
        param1, param2 = row[0], row[1]
        parameterPet[(param1, param2)].append(row)
    
    num = sum(len(v) for v in parameterPet.values())
    
    pbar = tqdm(total=num, desc=f"进程 {int(part)} ", position=part)
    #for key, value in tqdm.tqdm(parameterPet.items(), desc=f"波长 {wav*1e9:.0f} nm 扫参"):
    
    wav=[0.532e-6,0.800e-6]
    
    for key, value in parameterPet.items():
        p,h=key[0],key[1]
        ms.setMetaFdtd(fdtd, p, p, 1e-6, -0.5e-6)
        ms.classicMonitorGroup(fdtd, p, p, 1e-6)
        ms.addMetaBase(fdtd, "SiO2 (Glass) - Palik", p, p, 0.5e-6)
        for parameter in value:
            l=parameter[2] # 十字结构长度
            w=parameter[3] # 十字结构宽度
            r=parameter[4] # 中心圆半径
            
            adv.fishnetset(fdtd, "SiO2 (Glass) - Palik", h, l, w, r, name="Group")
            
            main=np.array([[p,h,l,w,r]])
            
            ms.addMetaSource(fdtd, p, p, -0.25e-6, wav[1], name="source")
            fdtd.run()
            data532 = ms.classicDataAcquisition(fdtd)
            fdtd.switchtolayout()
            
            adv.swichWaveLength(fdtd, wav[0], "source")
            fdtd.run()
            data800 = ms.classicDataAcquisition(fdtd)
            fdtd.switchtolayout()
                    
            Analysis=np.concatenate((main, data532, data800),axis=1)
            data = np.concatenate((data, Analysis),axis=0)
            fdtd.select("Group")
            fdtd.delete()
            
            pbar.update(1)

        fdtd.deleteall()
        
    pbar.close()
    print(data)
    return data

if __name__ == "__main__":
    print("扫参正在启动")
    # SQLite数据库准备
    conn = sqlite3.connect("structures.db")
    cursor = conn.cursor()
    #"SiO2 (Glass) - Palik"

    # 计算参数
    parallelsNum=2
    
    P=np.linspace(0.2e-6,0.5e-6,4)
    H=np.linspace(0.2e-6,0.8e-6,4)
    L=np.linspace(0.04e-6,0.4e-6,2)
    W=np.linspace(0.04e-6,0.4e-6,3)
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
                                
    parameter=split_matrix(allParameterPet,parallelsNum)
    
    processes = []
    for i in range(parallelsNum):
        iterations=parameter[i]
        p = multiprocessing.Process(target=simulation, args=(iterations,i)) # iterations为此次并行进程中使用的参数，i为进程id
        processes.append(p)
        
    for p in processes:
        p.start()
            
    for p in processes:
        p.join()